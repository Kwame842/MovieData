# 🚑 Real-Time Customer Heartbeat Monitoring System

## 🧠 Overview  
This project simulates real-time heart rate data, streams it using Kafka, processes it through a Kafka consumer, stores it in a PostgreSQL database, and visualizes the data with Grafana.

---

## 🧩 System Components

- **Producer** (`kafka_client/producer.py`): Simulates and streams synthetic heartbeat data to Kafka.  
- **Kafka**: Manages real-time messaging between the producer and consumer.  
- **Consumer** (`kafka_client/consumer.py`): Consumes Kafka messages and stores validated records in PostgreSQL.  
- **PostgreSQL**: Stores heartbeat data.  
- **Grafana**: Visualizes heartbeat trends in real time using PostgreSQL as a data source.

---

## 🚀 Quick Start (Dockerized)

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd heartbeat-monitoring
```

### 2️⃣ Launch the Full Stack
```bash
docker compose up --build
```

This will start:

- Kafka + Zookeeper  
- PostgreSQL (with initial schema)  
- Producer and Consumer services  
- Grafana dashboard (accessible at port `3000`)

### 3️⃣ Access Grafana Dashboard  
- URL: [http://localhost:3000](http://localhost:3000)  
- Default Login:
  - **Username**: `admin`  
  - **Password**: `admin` *(you'll be prompted to change it)*

---

## 📊 Grafana Setup Guide

1. Navigate to **Configuration → Data Sources**
2. Add a **PostgreSQL** data source:
   - **Host**: `postgres:****`
   - **Database**: `heartbeats`
   - **User**: `*****`
   - **Password**: `*******`
   - **SSL**: *Disable*
3. Create a new panel with the following query:
   ```sql
   SELECT
     timestamp AS "time",
     bpm AS heart_rate
   FROM heartbeats
   ORDER BY timestamp DESC
   LIMIT 100;
   ```
4. Choose **Time Series** as the visualization type.

---

## 🧱 Directory Structure

```
heartbeat-monitoring/
├── docker-compose.yml
├── kafka_client/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── producer.py
│   ├── consumer.py
│   └── db/
│       └── schema.sql
├── dashboard/
│   └── app.py
├── diagram/
│   └── Data_pipeline_architecture.png
├── docs/
├── screenshots/
└── README.md
```

---

## ⚙️ Tech Stack

- Python (`kafka-python`, `psycopg2`)
- Apache Kafka
- PostgreSQL
- Grafana
- Docker Compose

---

## 📦 Requirements (If Running Manually)

- `kafka-python`  
- `psycopg2-binary`  
- `pandas`

---

## 📷 Screenshots & Architecture

Dashboard previews and system architecture diagrams are available under the `docs/` and `diagram/` directories.
