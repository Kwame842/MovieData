# ✈️ Airflow Docker Project – PostgreSQL & MySQL Integration

This project sets up an Apache Airflow environment using Docker Compose with support for:

- PostgreSQL as the metadata database
- MySQL as a data source (e.g., `flight_staging`)
- Custom configuration and Python packages
- A clean structure for DAGs, plugins, and configs

## 📁 Project Structure

```
.
├── config/                    # Custom config modules
│   ├── __init__.py
│   └── settings.py
├── dags/                      # DAGs live here
│   └──flight_price_pipeline.py
├── diagram/                   # Architecture diagram
├── docker/
│       └──mysql               # Database and configurations
├── plugins/                   # Custom operators, helpers, etc.
├── scrrenshots/               # Screenshots of the Airflow UI
├── data/                      # Any input/output data
├── logs/                      # Airflow logs
├── docker-compose.yml         # Docker Compose services
├── requirements.txt            # Python dependencies
├── Dockerfile                 # Custom Airflow image
└── README.md
```

---

## 🚀 Features

- **PostgreSQL**: Metadata database for Airflow.
- **MySQL**: Staging database initialized via `init.sql`.
- **Custom Configuration**: Use `config/settings.py` in DAGs via clean import paths.
- **LocalExecutor**: Run tasks in parallel for small to medium workloads.
- **Basic Auth**: Log in via username/password (`admin:admin` by default).

---

## 🛠️ Prerequisites

- Docker & Docker Compose installed

---

## 🔧 Configuration

### `Dockerfile`

Custom image built from `apache/airflow:2.8.1-python3.10`, extended with required system packages and custom modules:

```dockerfile
FROM apache/airflow:2.8.1-python3.10

USER root
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

USER airflow

COPY ./dags /opt/airflow/dags
COPY ./plugins /opt/airflow/plugins
COPY ./config /opt/airflow/config

ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/config:/opt/airflow/plugins"
```

### Docker Compose Environment (`docker-compose.yml`)

Key settings include:

- PostgreSQL container with health check
- MySQL container initialized with an SQL script
- Airflow Webserver and Scheduler sharing code/config
- PYTHONPATH correctly set for custom imports

Update:

```yaml
- AIRFLOW__CORE__PYTHONPATH=/opt/airflow/config:/opt/airflow/plugins
```

---

## 🧪 Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-repo/airflow-docker-mysql-postgres.git
   cd airflow-docker-mysql-postgres
   ```

2. **Create init files if missing**

   ```bash
   touch config/__init__.py
   ```

3. **Build & run containers**

   ```bash
   docker-compose down --volumes --remove-orphans
   docker-compose build
   docker-compose up
   ```

4. **Access Airflow UI**  
   Go to [http://localhost:8080](http://localhost:8080)  
   Login:
   - Username: `admin`
   - Password: `admin`

---

## ✅ DAG Example

In any DAG, you can safely import config like this:

```python
from config.settings import settings
```

Make sure `settings.py` contains your structured configuration, e.g.,:

```python
# config/settings.py
settings = {
    "source_db": "mysql",
    "target_db": "postgres"
}
```

---

## 🧹 Cleaning Up

Stop and remove all containers and volumes:

```bash
docker-compose down --volumes --remove-orphans
```

---

## 📬 Feedback & Contribution

Feel free to fork, improve, and submit pull requests. For issues, please open a GitHub issue.

---

## 📄 License

MIT License. See `LICENSE` file.
