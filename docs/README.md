🚑 Real-Time Customer Heartbeat Monitoring System
🧠 Overview
This project simulates real-time heart rate data, streams it via Kafka, processes it through a Kafka consumer, stores it in a PostgreSQL database, and visualizes the data using Grafana.

🧩 System Components
Producer (kafka_client/producer.py): Simulates and streams synthetic heartbeats to Kafka.

Kafka: Handles real-time messaging between producer and consumer.

Consumer (kafka_client/consumer.py): Consumes Kafka messages and stores validated records into PostgreSQL.

PostgreSQL: Stores the heartbeat data.

Grafana: Visualizes heartbeat trends in real time using data from PostgreSQL.

🚀 Quick Start (Dockerized)
1️⃣ Clone the repository
bash
Copy
Edit
git clone <your-repo-url>
cd heartbeat-monitoring
2️⃣ Start the full stack with Docker
bash
Copy
Edit
docker compose up --build
This will launch:

Kafka + Zookeeper

PostgreSQL (with initial schema)

Producer and Consumer services

Grafana dashboard (port 3000)

3️⃣ Access Grafana Dashboard
URL: http://localhost:3000

Default login:
Username: admin
Password: admin (you'll be asked to change it)

📊 Grafana Setup Guide
Go to Configuration → Data Sources

Add a PostgreSQL data source:

Host: postgres:5432

Database: heartbeats

User: postgres

Password: pgpass007

SSL: Disable

Create a panel with the following query:

sql
Copy
Edit
SELECT
  timestamp AS "time",
  bpm AS heart_rate
FROM heartbeats
ORDER BY timestamp DESC
LIMIT 100;
Choose Time Series as the visualization type.

🧱 Directory Structure
pgsql
Copy
Edit
heartbeat-monitoring/
├── docker-compose.yml
├── kafka_client/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── producer.py
│   ├── consumer.py
│   └── db/
│       └── schema.sql
├── grafana_data/ (volume)
⚙️ Tech Stack
Python (kafka-python, psycopg2)

Apache Kafka

PostgreSQL

Grafana

Docker Compose

📦 Requirements (if running manually)
txt
Copy
Edit
kafka-python
psycopg2-binary
pandas
📷 Screenshots & Architecture
Dashboard and system architecture available under docs/ (if applicable)
