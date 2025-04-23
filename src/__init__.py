# Initialize the src package
from .config import load_config
from .data_processing import fetch_movie_data, clean_movie_data
from .analysis import analyze_movies, visualize_results

__all__ = [
    'load_config',
    'fetch_movie_data',
    'clean_movie_data',
    'analyze_movies',
    'visualize_results'
]
