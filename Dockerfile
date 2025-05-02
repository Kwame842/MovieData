# Use official Python image with Java preinstalled
FROM bitnami/spark:latest

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install required Python packages
USER root
RUN pip install --upgrade pip && \
    pip install pyspark

# Create app directory and copy the script
WORKDIR /app
COPY Spark_Streaming_to_Postgres_New.py .

# Create directory for incoming CSV files (mounted later)
RUN mkdir /data

# Set the default command
CMD ["spark-submit", "Spark_Streaming_to_Postgres_New.py"]
