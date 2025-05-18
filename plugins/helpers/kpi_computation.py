import logging
from typing import List, Dict, Any
import pandas as pd
from config.settings import settings
from plugins.helpers.database_utils import get_mysql_connection, execute_sql
import os

# Configure logging
logging.basicConfig(
    filename=os.path.join(settings.LOG_DIR, 'kpi_computation.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def compute_airline_kpis() -> List[Dict[str, Any]]:
    """Compute KPIs by airline."""
    try:
        query = """
        SELECT 
            airline,
            AVG(total_fare) as avg_fare,
            COUNT(*) as booking_count
        FROM flight_price_staging
        WHERE processed = FALSE
        GROUP BY airline
        ORDER BY booking_count DESC;
        """
        
        with get_mysql_connection() as conn:
            results = execute_sql(conn, query, fetch=True)
        
        kpis = [{
            'airline': row[0],
            'avg_fare': float(row[1]),
            'booking_count': int(row[2])
        } for row in results]
        
        logger.info(f"Computed airline KPIs for {len(kpis)} airlines")
        return kpis
    
    except Exception as e:
        logger.error(f"Error computing airline KPIs: {e}", exc_info=True)
        raise

def compute_route_kpis() -> List[Dict[str, Any]]:
    """Compute KPIs by route (source-destination pairs)."""
    try:
        query = """
        SELECT 
            source,
            destination,
            COUNT(*) as booking_count,
            AVG(total_fare) as avg_fare
        FROM flight_price_staging
        WHERE processed = FALSE
        GROUP BY source, destination
        ORDER BY booking_count DESC
        LIMIT 10;
        """
        
        with get_mysql_connection() as conn:
            results = execute_sql(conn, query, fetch=True)
        
        kpis = [{
            'source': row[0],
            'destination': row[1],
            'booking_count': int(row[2]),
            'avg_fare': float(row[3])
        } for row in results]
        
        logger.info(f"Computed route KPIs for {len(kpis)} routes")
        return kpis
    
    except Exception as e:
        logger.error(f"Error computing route KPIs: {e}", exc_info=True)
        raise

def compute_seasonal_kpis() -> List[Dict[str, Any]]:
    """Compute seasonal fare variation KPIs."""
    try:
        query = """
        SELECT 
            CASE 
                WHEN is_peak_season THEN 'Peak Season'
                ELSE 'Non-Peak Season'
            END as season_type,
            AVG(total_fare) as avg_fare,
            COUNT(*) as booking_count
        FROM flight_price_staging
        WHERE processed = FALSE
        GROUP BY season_type;
        """
        
        with get_mysql_connection() as conn:
            results = execute_sql(conn, query, fetch=True)
        
        kpis = [{
            'season_type': row[0],
            'avg_fare': float(row[1]),
            'booking_count': int(row[2])
        } for row in results]
        
        logger.info("Computed seasonal KPIs")
        return kpis
    
    except Exception as e:
        logger.error(f"Error computing seasonal KPIs: {e}", exc_info=True)
        raise

def mark_records_as_processed():
    """Mark processed records in the staging table."""
    try:
        update_query = """
        UPDATE flight_price_staging
        SET processed = TRUE
        WHERE processed = FALSE;
        """
        
        with get_mysql_connection() as conn:
            execute_sql(conn, update_query)
        
        logger.info("Marked records as processed in staging table")
    
    except Exception as e:
        logger.error(f"Error marking records as processed: {e}", exc_info=True)
        raise