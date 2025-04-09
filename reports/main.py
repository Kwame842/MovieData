#!/usr/bin/env python3
"""
TMDB Movie Data Analysis - Main Script
Fetches, analyzes, and visualizes movie data from TMDB API.
"""

import os
from dotenv import load_dotenv
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

# Constants
BASE_URL = "https://api.themoviedb.org/3/movie/"
MOVIE_IDS = [0, 299534, 19995, 140607, 299536, 597, 135397, 420818, 24428, 
             168259, 99861, 284054, 12445, 181808, 330457, 351286, 109445, 
             321612, 260513]

def load_api_key():
    """Load API key from .env file with validation"""
    load_dotenv()
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        raise ValueError("API key not found in .env file. Please add TMDB_API_KEY=your_key")
    return api_key

def fetch_movie_data(movie_id, api_key):
    """Fetch movie data from TMDB API with error handling"""
    try:
        url = f"{BASE_URL}{movie_id}?api_key={api_key}&append_to_response=credits"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie ID {movie_id}: {str(e)}")
        return None

def process_movie_data(raw_data):
    """Clean and transform raw movie data"""
    if not raw_data:
        return None
        
    # Extract relevant fields
    movie = {
        'id': raw_data.get('id'),
        'title': raw_data.get('title'),
        'budget': raw_data.get('budget'),
        'revenue': raw_data.get('revenue'),
        'runtime': raw_data.get('runtime'),
        'vote_average': raw_data.get('vote_average'),
        'vote_count': raw_data.get('vote_count'),
        'popularity': raw_data.get('popularity'),
        'release_date': raw_data.get('release_date'),
        'genres': "|".join([g['name'] for g in raw_data.get('genres', [])]),
        'collection': raw_data.get('belongs_to_collection', {}).get('name'),
        'director': next((crew['name'] for crew in raw_data.get('credits', {}).get('crew', []) 
                         if crew.get('job') == 'Director'), None)
    }
    
    # Convert financials to millions USD
    for field in ['budget', 'revenue']:
        movie[f"{field}_musd"] = movie[field] / 1_000_000 if movie[field] else None
    
    return movie

def generate_visualizations(df):
    """Create and save analysis visualizations"""
    plt.style.use('seaborn')
    
    # 1. Revenue vs Budget
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='budget_musd', y='revenue_musd', hue='collection', 
                    palette='viridis', s=100)
    plt.title("Revenue vs Budget by Franchise Status")
    plt.xlabel("Budget (Million USD)")
    plt.ylabel("Revenue (Million USD)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('reports/figures/revenue_vs_budget.png')
    plt.close()
    
    # 2. ROI by Genre (sample visualization)
    df['roi'] = df['revenue_musd'] / df['budget_musd']
    genre_roi = df.explode('genres').groupby('genres')['roi'].median().sort_values()
    
    plt.figure(figsize=(12, 6))
    genre_roi.plot(kind='barh', color='skyblue')
    plt.title("Median ROI by Genre")
    plt.xlabel("Return on Investment (Revenue/Budget)")
    plt.tight_layout()
    plt.savefig('reports/figures/roi_by_genre.png')
    plt.close()

def main():
    """Main execution function"""
    # Setup directories
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('reports/figures', exist_ok=True)
    
    # Load API key
    api_key = load_api_key()
    
    # Fetch and process data
    print("Fetching movie data from TMDB API...")
    movies = []
    for movie_id in tqdm(MOVIE_IDS):
        raw_data = fetch_movie_data(movie_id, api_key)
        if raw_data:
            movies.append(process_movie_data(raw_data))
    
    # Create DataFrame
    df = pd.DataFrame([m for m in movies if m])
    df.to_csv('data/processed/movies_clean.csv', index=False)
    
    # Analysis and visualization
    print("Generating visualizations...")
    generate_visualizations(df)
    
    print("\nAnalysis complete!")
    print(f"Processed {len(df)} movies. Results saved to:")
    print("- data/processed/movies_clean.csv")
    print("- reports/figures/")

if __name__ == "__main__":
    main()