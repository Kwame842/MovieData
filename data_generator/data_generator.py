import random, time, json
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def generate_heartbeat():
    return {
        "customer_id": random.randint(1, 10),
        "timestamp": datetime.utcnow().isoformat(),
        "heart_rate": random.randint(50, 120)
    }

while True:
    heartbeat = generate_heartbeat()
    producer.send('heartbeat', value=heartbeat)
    print("Produced:", heartbeat)
    time.sleep(1)
