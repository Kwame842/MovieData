
FROM apache/airflow:2.8.1-python3.10

# Install extra packages if needed (e.g., mysqlclient, psycopg2)
USER root
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy your project files
COPY ./dags /opt/airflow/dags
COPY ./plugins /opt/airflow/plugins
COPY ./config /opt/airflow/config

# Set PYTHONPATH so Airflow can find the `config` and `plugins` packages
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/config:/opt/airflow/plugins"