import logging
from contextlib import contextmanager
from typing import Dict, Any
import mysql.connector
import psycopg2
from mysql.connector import Error as MySQLError
from psycopg2 import Error as PostgreSQLError
from config.settings import settings
import os

# Configure logging
logging.basicConfig(
    filename=os.path.join(settings.LOG_DIR, 'database_operations.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@contextmanager
def get_mysql_connection():
    """Context manager for MySQL database connections."""
    conn = None
    try:
        conn = mysql.connector.connect(**settings.DB_CONFIG['mysql'])
        yield conn
    except MySQLError as e:
        logger.error(f"MySQL connection error: {e}", exc_info=True)
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()

@contextmanager
def get_postgresql_connection():
    """Context manager for PostgreSQL database connections."""
    conn = None
    try:
        conn = psycopg2.connect(**settings.DB_CONFIG['postgresql'])
        yield conn
    except PostgreSQLError as e:
        logger.error(f"PostgreSQL connection error: {e}", exc_info=True)
        raise
    finally:
        if conn and conn.closed == 0:
            conn.close()

def execute_sql(conn, query: str, params: tuple = None, fetch: bool = False):
    """Generic SQL execution function with error handling."""
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        
        if fetch:
            return cursor.fetchall()
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"SQL execution error: {e}\nQuery: {query}", exc_info=True)
        raise
    finally:
        if cursor:
            cursor.close()

def create_mysql_staging_table():
    """Create the staging table in MySQL if it doesn't exist."""
    create_table_query = """
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
    """
    
    with get_mysql_connection() as conn:
        execute_sql(conn, create_table_query)

def create_postgresql_analytics_tables():
    """Create analytics tables in PostgreSQL."""
    queries = [
        """
        CREATE TABLE IF NOT EXISTS airline_kpi (
            id SERIAL PRIMARY KEY,
            airline VARCHAR(100),
            avg_fare DECIMAL(10, 2),
            booking_count INTEGER,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS route_kpi (
            id SERIAL PRIMARY KEY,
            source VARCHAR(100),
            destination VARCHAR(100),
            booking_count INTEGER,
            avg_fare DECIMAL(10, 2),
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS seasonal_kpi (
            id SERIAL PRIMARY KEY,
            season_type VARCHAR(50),
            avg_fare DECIMAL(10, 2),
            booking_count INTEGER,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]
    
    with get_postgresql_connection() as conn:
        for query in queries:
            execute_sql(conn, query)