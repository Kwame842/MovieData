import json
import logging
from kafka import KafkaConsumer
from kafka.errors import KafkaError, NoBrokersAvailable
from db.db_insert import insert_heartbeat

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

def create_kafka_consumer(topic='heartbeat', bootstrap_servers='127.0.0.1:9092'):
    """Initialize and return a Kafka consumer."""
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='latest',
            enable_auto_commit=True
        )
        logging.info(f"Kafka consumer subscribed to topic '{topic}'")
        return consumer
    except NoBrokersAvailable:
        logging.critical("Kafka broker not available. Is Kafka running on 127.0.0.1:9092?")
        raise
    except Exception as e:
        logging.critical(f"Failed to create Kafka consumer: {e}")
        raise

def process_message(data):
    """Process a single Kafka message."""
    try:
        logging.debug(f"Consumed message: {data}")
        if 40 <= data["heart_rate"] <= 180:
            logging.info(f"Inserting valid heartbeat: {data}")
            insert_heartbeat(data)
            logging.info("Inserted successfully.")
        else:
            logging.warning(f"Anomalous heartbeat detected: {data}")
    except Exception as e:
        logging.error(f"Failed to process message: {e}")

def consume_heartbeat_messages():
    """Main loop to consume and process messages from Kafka."""
    try:
        consumer = create_kafka_consumer()
    except Exception:
        logging.error("Exiting due to Kafka connection failure.")
        return

    logging.info("Listening for heartbeat messages... Press Ctrl+C to stop.")
    try:
        for message in consumer:
            process_message(message.value)
    except KeyboardInterrupt:
        logging.info("Kafka consumer stopped by user.")
    except KafkaError as e:
        logging.error(f"Kafka error while consuming messages: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while consuming messages: {e}")
    finally:
        consumer.close()
        logging.info("Kafka consumer closed.")

if __name__ == "__main__":
    consume_heartbeat_messages()
