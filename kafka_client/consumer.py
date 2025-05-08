from kafka import KafkaConsumer
import json
from db.db_insert import insert_heartbeat

# Initialize Kafka consumer to read messages from 'heartbeat' topic
consumer = KafkaConsumer('heartbeat', bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

# Consume messages from Kafka
for message in consumer:
    data = message.value
    
    # Debugging: print the consumed message
    print("Consumed message:", data)
    
    # Check if the heart_rate is within the normal range
    if 40 <= data["heart_rate"] <= 180:  # Basic anomaly check
        print(f"Inserting valid data: {data}")  # Debugging: Confirm valid data is being processed
        insert_heartbeat(data)  # Call the function to insert data into the database
        print("Inserted heartbeat:", data)  # Debugging: Confirm insertion
    else:
        print("Anomalous reading:", data)  # Debugging: Print anomalous readings
