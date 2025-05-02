import csv
import time
import random
import os
from datetime import datetime
import uuid

# Configuration
OUTPUT_DIR = "ecommerce_events"
EVENT_TYPES = ["view", "purchase"]
PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Smartphone", "price": 599.99},
    {"id": 3, "name": "Headphones", "price": 99.99},
]

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def generate_event():
    """Generate a single e-commerce event"""
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": random.randint(1000, 9999),
        "event_type": random.choice(EVENT_TYPES),
        "product_id": random.choice(PRODUCTS)["id"],
        "product_name": random.choice(PRODUCTS)["name"],
        "price": random.choice(PRODUCTS)["price"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def write_event_to_csv():
    """Write events to CSV file"""
    filename = f"{OUTPUT_DIR}/events_{int(time.time())}.csv"
    event = generate_event()
    
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ["event_id", "user_id", "event_type", "product_id", 
                     "product_name", "price", "timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(event)
    
    print(f"Generated: {filename}")

def main():
    """Main function to continuously generate events"""
    try:
        while True:
            write_event_to_csv()
            time.sleep(2)  # Generate event every 2 seconds
    except KeyboardInterrupt:
        print("Stopped generating events")

if __name__ == "__main__":
    main()