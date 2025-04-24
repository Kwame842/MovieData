from pyspark.sql import functions as F
from pyspark.sql.types import *
import requests
import json
from .config import load_config

config = load_config()

def fetch_movie_data(movie_ids):
    """Fetch movie data from TMDB API"""
    movies = []
    for movie_id in movie_ids:
        try:
            url = f"{config['base_url']}{movie_id}?api_key={config['api_key']}"
            response = requests.get(url)
            if response.status_code == 200:
                movies.append(response.json())
            else:
                print(f"Failed to fetch data for movie ID {movie_id}")
        except Exception as e:
            print(f"Error fetching movie {movie_id}: {str(e)}")
    
    return movies

def clean_movie_data(spark, movies_data):
    """Clean and preprocess movie data"""
    # Create DataFrame
    df = spark.createDataFrame(movies_data)
    
    # Drop irrelevant columns
    cols_to_drop = ['adult', 'imdb_id', 'original_title', 'video', 'homepage']
    df = df.drop(*cols_to_drop)
    
    # Process JSON columns
    json_columns = {
        'belongs_to_collection': 'name',
        'genres': 'name',
        'production_companies': 'name',
        'production_countries': 'iso_3166_1',
        'spoken_languages': 'iso_639_1'
    }
    
    for col_name, field in json_columns.items():
        if col_name == 'belongs_to_collection':
            df = df.withColumn(col_name, 
                F.when(F.col(col_name).isNull(), None)
                .otherwise(F.col(f"{col_name}.{field}")))
        else:
            df = df.withColumn(col_name, 
                F.array_join(F.expr(f"transform({col_name}, x -> x.{field})"), "|"))
    
    # Convert data types
    df = (df
        .withColumn("budget", F.col("budget").cast("double"))
        .withColumn("revenue", F.col("revenue").cast("double"))
        .withColumn("popularity", F.col("popularity").cast("double"))
        .withColumn("vote_count", F.col("vote_count").cast("integer"))
        .withColumn("vote_average", F.col("vote_average").cast("double"))
        .withColumn("release_date", F.to_date("release_date", "yyyy-MM-dd"))
    )
    
    # Handle missing values
    df = (df
        .withColumn("budget", 
            F.when((F.col("budget") == 0) | F.col("budget").isNull(), None)
            .otherwise(F.col("budget")))
        .withColumn("revenue", 
            F.when((F.col("revenue") == 0) | F.col("revenue").isNull(), None)
            .otherwise(F.col("revenue")))
        .withColumn("vote_average", 
            F.when(F.col("vote_count") == 0, None)
            .otherwise(F.col("vote_average")))
    )
    
    # Convert to millions USD
    df = (df
        .withColumn("budget_musd", F.col("budget") / 1e6)
        .withColumn("revenue_musd", F.col("revenue") / 1e6)
    )
    
    # Filter and select columns
    final_columns = [
        'id', 'title', 'tagline', 'release_date', 'genres', 
        'belongs_to_collection', 'original_language', 'budget_musd', 
        'revenue_musd', 'production_companies', 'production_countries', 
        'vote_count', 'vote_average', 'popularity', 'runtime', 'overview', 
        'spoken_languages', 'poster_path'
    ]
    
    return df.filter(F.col("status") == "Released") \
             .drop("status") \
             .select(*final_columns)
