# User Guide: Running the Ecommerce Data Pipeline

## Prerequisites

- Python 3.8+
- Apache Spark 3.5.0
- PostgreSQL 15
- Java 11
- Required Python packages: `pyspark`, `uuid`

## Setup Instructions

1. **Install Dependencies**

   ```bash
   pip install pyspark uuid
   ```

2. **Setup PostgreSQL**

   - Install PostgreSQL
   - Run `postgres_setup.sql`:
     ```bash
     psql -U postgres -f postgres_setup.sql
     ```

3. **Configure Spark**
   - Download PostgreSQL JDBC driver (42.7.3)
   - Add to Spark's jars directory

## Running the Pipeline

1. **Start Data Generator**

   ```bash
   python data_generator.py
   ```

2. **Run Spark Streaming Job**

   ```bash
   spark-submit spark_streaming_to_postgres.py
   ```

3. **Verify Data in PostgreSQL**
   ```sql
   SELECT * FROM events LIMIT 10;
   ```

## Stopping the Pipeline

- Press Ctrl+C in the data generator terminal
- Stop the Spark job
