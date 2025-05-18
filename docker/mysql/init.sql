CREATE DATABASE IF NOT EXISTS flight_staging;
CREATE DATABASE IF NOT EXISTS flight_analytics;

CREATE USER IF NOT EXISTS 'airflow'@'%' IDENTIFIED BY 'airflow';
GRANT ALL PRIVILEGES ON flight_staging.* TO 'airflow'@'%';
GRANT ALL PRIVILEGES ON flight_analytics.* TO 'airflow'@'%';
FLUSH PRIVILEGES;

USE flight_staging;

CREATE TABLE IF NOT EXISTS flight_price_staging (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airline VARCHAR(100),
    source VARCHAR(100),
    destination VARCHAR(100),
    base_fare DECIMAL(10, 2),
    tax_surcharge DECIMAL(10, 2),
    total_fare DECIMAL(10, 2),
    travel_date DATE,
    booking_date DATE,
    flight_duration VARCHAR(50),
    is_peak_season BOOLEAN DEFAULT FALSE,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

USE flight_analytics;

CREATE TABLE IF NOT EXISTS airline_kpi (
    id SERIAL PRIMARY KEY,
    airline VARCHAR(100),
    avg_fare DECIMAL(10, 2),
    booking_count INTEGER,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS route_kpi (
    id SERIAL PRIMARY KEY,
    source VARCHAR(100),
    destination VARCHAR(100),
    booking_count INTEGER,
    avg_fare DECIMAL(10, 2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS seasonal_kpi (
    id SERIAL PRIMARY KEY,
    season_type VARCHAR(50),
    avg_fare DECIMAL(10, 2),
    booking_count INTEGER,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);