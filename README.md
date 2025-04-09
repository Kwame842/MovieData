# MovieData
TMDB Movie Data Analysis Project
Project Overview
This project analyzes movie data from The Movie Database (TMDB) API to uncover insights about film performance, genre profitability, and franchise success. The analysis includes data collection, cleaning, exploratory analysis, and visualization of key metrics.

Prerequisites
Before running the project, ensure you have the following installed:

Python 3.8+

pip (Python package manager)

Jupyter Notebook (optional, for interactive analysis)

Installation
Clone the repository:


git clone https://github.com/Kwame842/MovieData.git
cd tmdb-movie-analysis
Create and activate a virtual environment (recommended):


python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install required packages:


pip install -r requirements.txt
Configuration
Obtain a TMDB API key:

Register at https://www.themoviedb.org/settings/api

Create a .env file in the project root and add your API key:


TMDB_API_KEY=your_api_key_here
Running the Analysis
Option 1: Run as Jupyter Notebook
Start Jupyter Notebook:

bash
Copy
jupyter notebook
Open movie_analysis.ipynb

Run all cells sequentially

Option 2: Run as Python Script
bash
Copy
python main.py
Project Structure
Copy
tmdb-movie-analysis/
├── data/                   # Contains raw and processed data files
│   ├── raw/                # Raw JSON responses from API
│   └── processed/          # Cleaned CSV files
├── notebooks/              # Jupyter notebooks for analysis
│   └── movie_analysis.ipynb
├── scripts/                # Python modules
│   ├── data_fetch.py       # API data collection
│   ├── data_clean.py       # Data cleaning and processing
│   ├── analysis.py         # Analytical functions
│   └── visualization.py    # Plot generation
├── reports/                # Generated reports and visualizations
├── .env.example            # Example environment config
├── requirements.txt        # Python dependencies
├── main.py                 # Main executable script
└── README.md               # This file
Key Features
Fetches movie data from TMDB API

Cleans and preprocesses raw JSON data

Performs financial and ratings analysis

Generates visualizations:

Revenue vs Budget scatter plots

ROI by genre boxplots

Yearly trends in film economics

Popularity vs Rating analysis

Outputs
Running the project will generate:

Data files in data/processed/:

movies_clean.csv - Cleaned dataset

franchise_stats.csv - Franchise performance metrics

Visualizations in reports/figures/:

Revenue vs Budget plots

Genre ROI distributions

Yearly trends charts

Popularity-Rating relationships

Analysis report in reports/:

analysis_report.pdf - Summary of key findings

Troubleshooting
Common issues and solutions:

API Limit Errors:

TMDB has rate limits (typically 40 requests/10 seconds)

Solution: Add delays between requests or request higher limits

Missing Data:

Some movies may have incomplete financial data

Solution: Script automatically handles missing values

Authentication Errors:

Ensure your API key is correctly set in .env

Verify the key has proper permissions

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Open a pull request

License
This project is licensed under the MIT License - see the LICENSE file for details.
