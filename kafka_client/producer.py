from kafka import KafkaProducer  # ← this now correctly imports from kafka-python

import sys, os
# ensure the project root is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import time
import json
from kafka import KafkaProducer
from data_generator.data_generator import generate_heartbeat

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_name = 'heartbeat'

print(f"[Producer] Sending data to topic '{topic_name}'... Press Ctrl+C to stop.")

try:
    while True:
        data = generate_heartbeat()
        producer.send(topic_name, value=data)
        print(f"[Producer] Sent: {data}")
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[Producer] Stopped.")
finally:
    producer.flush()
    producer.close()
