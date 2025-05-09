import random
import time
import json
import logging
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def create_kafka_producer(bootstrap_servers='localhost:9092'):
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        logger.info("Kafka producer created successfully.")
        return producer
    except KafkaError as e:
        logger.exception("Failed to create Kafka producer.")
        raise

def generate_heartbeat():
    return {
        "customer_id": random.randint(1, 10),
        "timestamp": datetime.utcnow().isoformat(),
        "heart_rate": random.randint(50, 120)
    }

def send_heartbeat(producer, topic='heartbeat'):
    heartbeat = generate_heartbeat()
    try:
        future = producer.send(topic, value=heartbeat)
        record_metadata = future.get(timeout=10)
        logger.info(f"Produced: {heartbeat} to topic {record_metadata.topic} partition {record_metadata.partition}")
    except KafkaError as e:
        logger.error("Failed to send heartbeat message.", exc_info=True)

def main():
    producer = create_kafka_producer()
    try:
        while True:
            send_heartbeat(producer)
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Heartbeat producer stopped by user.")
    except Exception as e:
        logger.exception("Unexpected error occurred.")
    finally:
        producer.close()
        logger.info("Kafka producer closed.")

if __name__ == "__main__":
    main()
