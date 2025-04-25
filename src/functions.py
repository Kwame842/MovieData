
import requests
from pyspark.sql.functions import expr, when, array_join

def fetch_movie_data(movie_id, base_url, api_key):
    """Fetch movie data from TMDB API for a given movie ID"""
    url = f"{base_url}{movie_id}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for movie ID {movie_id}")
        return None

def process_collection(col):
    """Extract collection name from JSON"""
    return when(
        col.isNull(), 
        None
    ).otherwise(
        expr("belongs_to_collection.name")
    ).alias("belongs_to_collection")

def process_json_array(col_name, field='name'):
    """Extract names from JSON array and join with |"""
    return array_join(
        expr(f"transform({col_name}, x -> x.{field})"),
        "|"
    ).alias(col_name)
