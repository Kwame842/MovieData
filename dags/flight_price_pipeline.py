from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from plugins.custom_operators.csv_to_mysql_operator import CSVToMySQLOperator 
from plugins.helpers.database_utils import create_mysql_staging_table, create_postgresql_analytics_tables
from plugins.helpers.kpi_computation import (
    compute_airline_kpis,
    compute_route_kpis,
    compute_seasonal_kpis,
    mark_records_as_processed
)
from config.settings import settings

default_args = settings.DEFAULT_ARGS

def load_kpis_to_postgres(kpis: list, table_name: str):
    """Helper function to load KPIs to PostgreSQL."""
    from plugins.helpers.database_utils import get_postgresql_connection, execute_sql
    
    if not kpis:
        return
    
    with get_postgresql_connection() as conn:
        # Clear existing data (optional, could also do upsert)
        execute_sql(conn, f"DELETE FROM {table_name}")
        
        # Prepare and execute insert statements
        for kpi in kpis:
            columns = ', '.join(kpi.keys())
            placeholders = ', '.join(['%s'] * len(kpi))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            execute_sql(conn, query, tuple(kpi.values()))

with DAG(
    'flight_price_analysis',
    default_args=default_args,
    description='End-to-end pipeline for flight price analysis',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['flight', 'analysis', 'bangladesh'],
) as dag:
    
    # Task to create required database tables
    create_tables = PythonOperator(
        task_id='create_database_tables',
        python_callable=lambda: (
            create_mysql_staging_table(),
            create_postgresql_analytics_tables()
        ),
        dag=dag,
    )
    
    # Task to load CSV data into MySQL staging
    load_csv_to_mysql = CSVToMySQLOperator(
        task_id='load_csv_to_mysql',
        csv_file_path=settings.DATA_FILE,
        table_name='flight_price_staging',
        dag=dag,
    )
    
    # Task to compute airline KPIs
    compute_airline_kpis_task = PythonOperator(
        task_id='compute_airline_kpis',
        python_callable=compute_airline_kpis,
        dag=dag,
    )
    
    # Task to load airline KPIs to PostgreSQL
    load_airline_kpis = PythonOperator(
        task_id='load_airline_kpis',
        python_callable=lambda **context: load_kpis_to_postgres(
            context['ti'].xcom_pull(task_ids='compute_airline_kpis'),
            'airline_kpi'
        ),
        dag=dag,
    )
    
    # Task to compute route KPIs
    compute_route_kpis_task = PythonOperator(
        task_id='compute_route_kpis',
        python_callable=compute_route_kpis,
        dag=dag,
    )
    
    # Task to load route KPIs to PostgreSQL
    load_route_kpis = PythonOperator(
        task_id='load_route_kpis',
        python_callable=lambda **context: load_kpis_to_postgres(
            context['ti'].xcom_pull(task_ids='compute_route_kpis'),
            'route_kpi'
        ),
        dag=dag,
    )
    
    # Task to compute seasonal KPIs
    compute_seasonal_kpis_task = PythonOperator(
        task_id='compute_seasonal_kpis',
        python_callable=compute_seasonal_kpis,
        dag=dag,
    )
    
    # Task to load seasonal KPIs to PostgreSQL
    load_seasonal_kpis = PythonOperator(
        task_id='load_seasonal_kpis',
        python_callable=lambda **context: load_kpis_to_postgres(
            context['ti'].xcom_pull(task_ids='compute_seasonal_kpis'),
            'seasonal_kpi'
        ),
        dag=dag,
    )
    
    # Task to mark records as processed
    mark_processed = PythonOperator(
        task_id='mark_records_processed',
        python_callable=mark_records_as_processed,
        dag=dag,
    )
    
    # Define task dependencies
    create_tables >> load_csv_to_mysql
    load_csv_to_mysql >> compute_airline_kpis_task >> load_airline_kpis
    load_csv_to_mysql >> compute_route_kpis_task >> load_route_kpis
    load_csv_to_mysql >> compute_seasonal_kpis_task >> load_seasonal_kpis
    [load_airline_kpis, load_route_kpis, load_seasonal_kpis] >> mark_processed