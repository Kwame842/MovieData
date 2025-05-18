from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from plugins.helpers.data_validation import validate_csv, clean_and_transform_data
from plugins.helpers.database_utils import get_mysql_connection, execute_sql
import pandas as pd
import logging
from config.settings import settings   
# from config import settings
import os

class CSVToMySQLOperator(BaseOperator):
    """
    Custom operator to load CSV data into MySQL with validation and transformation.
    """
    
    @apply_defaults
    def __init__(self, csv_file_path: str, table_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csv_file_path = csv_file_path
        self.table_name = table_name
        
        # Configure logging
        logging.basicConfig(
            filename=os.path.join(settings.LOG_DIR, 'csv_to_mysql_operator.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def execute(self, context):
        self.logger.info(f"Starting CSV to MySQL loading for file: {self.csv_file_path}")
        
        # Step 1: Validate CSV
        is_valid, validation_result = validate_csv(self.csv_file_path)
        if not is_valid:
            error_msg = f"CSV validation failed: {validation_result}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Step 2: Load and transform data
        try:
            df = pd.read_csv(self.csv_file_path)
            df = clean_and_transform_data(df)
            self.logger.info("Data transformation completed successfully")
        except Exception as e:
            self.logger.error(f"Error during data transformation: {e}", exc_info=True)
            raise
        
        # Step 3: Load data to MySQL
        try:
            with get_mysql_connection() as conn:
                cursor = conn.cursor()
                
                # Prepare data for insertion
                records = df.to_dict('records')
                
                insert_query = f"""
                INSERT INTO {self.table_name} (
                    airline, source, destination, base_fare, 
                    tax_surcharge, total_fare, travel_date, 
                    booking_date, flight_duration, is_peak_season
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """
                
                for record in records:
                    values = (
                        record.get('Airline'),
                        record.get('Source'),
                        record.get('Destination'),
                        record.get('Base Fare'),
                        record.get('Tax & Surcharge'),
                        record.get('Total Fare'),
                        record.get('travel_date', None),
                        record.get('booking_date', None),
                        record.get('flight_duration', None),
                        record.get('is_peak_season', False)
                    )
                    execute_sql(conn, insert_query, values)
                
                self.logger.info(f"Successfully loaded {len(records)} records into MySQL")
                
        except Exception as e:
            self.logger.error(f"Error loading data to MySQL: {e}", exc_info=True)
            raise