# Import required libraries
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure display options for pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Set up API access
BASE_URL = 'https://api.themoviedb.org/3/movie/'
API_KEY = os.getenv('TMDB_API_KEY')  # Get API key from environment variables

# Make sure to add this to your requests:
# headers = {'Authorization': f'Bearer {API_KEY}'}
# or as a parameter: params = {'api_key': API_KEY}


movie_ids = [0, 299534, 19995, 140607, 299536, 597, 135397, 420818, 24428, 
             168259, 99861, 284054, 12445, 181808, 330457, 351286, 109445, 
             321612, 260513]


def fetch_movie_data(movie_id, api_key):
    """Fetch movie data from TMDB API for a given movie ID"""
    try:
        url = f"{BASE_URL}{movie_id}?api_key={api_key}&append_to_response=credits"
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for movie ID {movie_id}: {e}")
        return None

# Fetch data for all movies
all_movies_data = []
for movie_id in movie_ids:
    movie_data = fetch_movie_data(movie_id, API_KEY)
    if movie_data:
        all_movies_data.append(movie_data)
    else:
        print(f"Skipping movie ID {movie_id} due to fetch error")

# Create DataFrame
movies_df = pd.json_normalize(all_movies_data)

