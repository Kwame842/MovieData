import os
from dotenv import load_dotenv
from pathlib import Path

def load_config():
    """Load configuration from .env file"""
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    
    config = {
        'api_key': os.getenv('TMDB_API_KEY'),
        'base_url': 'https://api.themoviedb.org/3/movie/',
        'spark_master': os.getenv('SPARK_MASTER', 'local[*]')
    }
    
    if not config['api_key']:
        raise ValueError("TMDB_API_KEY not found in environment variables")
        
    return config