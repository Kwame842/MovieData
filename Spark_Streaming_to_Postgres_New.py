import os
import time
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, IntegerType, TimestampType

# Spark session
spark = SparkSession.builder \
    .appName("CSVToPostgresStreamingWorkaround") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3") \
    .getOrCreate()

# Define your CSV schema
schema = StructType() \
    .add("event_time", TimestampType()) \
    .add("event_type", StringType()) \
    .add("product_id", IntegerType()) \
    .add("category_id", IntegerType()) \
    .add("category_code", StringType()) \
    .add("brand", StringType()) \
    .add("price", StringType()) \
    .add("user_id", IntegerType()) \
    .add("user_session", StringType())

# Folder to watch
# folder = r"C:\Users\Nana\Downloads\Spark Structured Streaming\ecommerce_events"
folder = "/app/ecommerce_events"


# Track processed files
processed = set()

while True:
    all_files = [f for f in os.listdir(folder) if f.endswith(".csv")]
    new_files = [f for f in all_files if f not in processed]

    for file in new_files:
        file_path = os.path.join(folder, file)
        print(f"📥 Processing new file: {file_path}")
        
        df = spark.read.csv(file_path, schema=schema, header=True)
        
        df.write \
            .format("jdbc") \
            #.option("url", "jdbc:postgresql://localhost:5432/ecommerce") \
            .option("url", "jdbc:postgresql://postgres:5432/ecommerce")
            .option("dbtable", "events") \
            .option("user", "postgres") \      # DB user
            .option("password", "pgpass007") \  # specify your DB password here/ this is a sample password
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()

        processed.add(file)
        print(f"✅ Done with: {file}")

    time.sleep(5)  # Check for new files every 5 seconds
