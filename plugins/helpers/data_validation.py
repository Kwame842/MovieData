import logging
import pandas as pd
from typing import Tuple, Dict, Any
from config.settings import settings
import os

# Configure logging
logging.basicConfig(
    filename=os.path.join(settings.LOG_DIR, 'data_validation.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {
    'Airline': str,
    'Source': str,
    'Destination': str,
    'Base Fare': float,
    'Tax & Surcharge': float,
    'Total Fare': float
}

def validate_csv(file_path: str) -> Tuple[bool, Dict[str, Any]]:
    """Validate the CSV file structure and content."""
    validation_result = {
        'is_valid': True,
        'missing_columns': [],
        'type_mismatches': {},
        'null_values': {},
        'negative_fares': 0,
        'invalid_records': 0
    }
    
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully loaded CSV file: {file_path}")
        
        # Check for missing columns
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            validation_result['missing_columns'] = missing_cols
            validation_result['is_valid'] = False
            logger.error(f"Missing required columns: {missing_cols}")
            return (False, validation_result)
        
        # Check data types
        for col, expected_type in REQUIRED_COLUMNS.items():
            if not pd.api.types.is_dtype_equal(df[col].dtype, expected_type):
                validation_result['type_mismatches'][col] = {
                    'expected': expected_type.__name__,
                    'actual': df[col].dtype
                }
                validation_result['is_valid'] = False
        
        # Check for null values
        null_cols = df.isnull().sum()
        for col, count in null_cols.items():
            if count > 0:
                validation_result['null_values'][col] = count
                validation_result['is_valid'] = False
        
        # Check for negative fares
        fare_cols = ['Base Fare', 'Tax & Surcharge', 'Total Fare']
        negative_fares = df[fare_cols].apply(lambda x: x < 0).sum().sum()
        if negative_fares > 0:
            validation_result['negative_fares'] = negative_fares
            validation_result['is_valid'] = False
        
        # Check for invalid city names (example validation)
        valid_cities = ['Dhaka', 'Chittagong', 'Sylhet', 'Cox\'s Bazar']
        invalid_source = ~df['Source'].isin(valid_cities)
        invalid_dest = ~df['Destination'].isin(valid_cities)
        
        if invalid_source.sum() > 0 or invalid_dest.sum() > 0:
            validation_result['invalid_records'] = invalid_source.sum() + invalid_dest.sum()
            validation_result['is_valid'] = False
        
        if not validation_result['is_valid']:
            logger.warning(f"Validation issues found: {validation_result}")
        else:
            logger.info("CSV validation passed successfully")
            
        return (validation_result['is_valid'], validation_result)
    
    except Exception as e:
        logger.error(f"Error during CSV validation: {e}", exc_info=True)
        validation_result['is_valid'] = False
        return (False, validation_result)

def clean_and_transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform the data before loading to staging."""
    try:
        # Fill missing values
        df.fillna({
            'Base Fare': 0,
            'Tax & Surcharge': 0,
            'Total Fare': df['Base Fare'] + df['Tax & Surcharge']
        }, inplace=True)
        
        # Correct negative fares
        fare_cols = ['Base Fare', 'Tax & Surcharge', 'Total Fare']
        df[fare_cols] = df[fare_cols].apply(lambda x: x.abs())
        
        # Calculate total fare if not provided
        if 'Total Fare' not in df.columns or df['Total Fare'].isnull().any():
            df['Total Fare'] = df['Base Fare'] + df['Tax & Surcharge']
        
        # Identify peak seasons (example: Eid and Winter holidays)
        # Assuming there's a 'travel_date' column in the dataset
        if 'travel_date' in df.columns:
            df['travel_date'] = pd.to_datetime(df['travel_date'])
            df['is_peak_season'] = df['travel_date'].apply(
                lambda x: x.month in [6, 7, 12]  # Example peak months
            )
        
        logger.info("Data cleaning and transformation completed successfully")
        return df
    
    except Exception as e:
        logger.error(f"Error during data cleaning: {e}", exc_info=True)
        raise