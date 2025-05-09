import sys
import os
import time
import json
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError, NoBrokersAvailable
from data_generator.data_generator import generate_heartbeat

# Ensure the project root is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

def create_kafka_producer(bootstrap_servers='127.0.0.1:9092'):
    """Create a Kafka producer instance."""
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        logging.info("Kafka producer initialized successfully.")
        return producer
    except NoBrokersAvailable:
        logging.critical("No Kafka brokers available. Is the Kafka server running on 127.0.0.1:9092?")
        raise
    except Exception as e:
        logging.critical(f"Error initializing Kafka producer: {e}")
        raise

def send_data_loop(producer, topic_name='heartbeat'):
    """Send generated data to Kafka in a loop."""
    logging.info(f"[Producer] Sending data to topic '{topic_name}'... Press Ctrl+C to stop.")
    try:
        while True:
            data = generate_heartbeat()
            producer.send(topic_name, value=data)
            logging.info(f"[Producer] Sent: {data}")
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("[Producer] Stopped by user.")
    except KafkaError as e:
        logging.error(f"Kafka error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        producer.flush()
        producer.close()
        logging.info("Kafka producer closed cleanly.")

def main():
    try:
        producer = create_kafka_producer()
        send_data_loop(producer)
    except Exception:
        logging.error("Exiting due to Kafka initialization failure.")

if __name__ == "__main__":
    main()
