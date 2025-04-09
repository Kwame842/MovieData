# 🎬 MovieData  
**TMDB Movie Data Analysis Project**

## 📌 Project Overview  
This project analyzes movie data from [The Movie Database (TMDB)](https://www.themoviedb.org/) API to uncover insights about film performance, genre profitability, and franchise success.  
The analysis includes:

- Data collection from TMDB API  
- Data cleaning and preprocessing  
- Exploratory data analysis  
- Visualization of key metrics

---

## 🛠️ Prerequisites  
Ensure the following are installed before running the project:

- Python 3.8+  
- `pip` (Python package manager)  
- Jupyter Notebook *(optional, for interactive analysis)*

---

## 🚀 Installation  

### 1. Clone the Repository  
```bash
git clone https://github.com/Kwame842/MovieData.git  
cd tmdb-movie-analysis
```

### 2. Create and Activate a Virtual Environment *(Recommended)*  
**Linux/Mac:**  
```bash
python -m venv venv  
source venv/bin/activate
```

**Windows:**  
```bash
python -m venv venv  
venv\Scripts\activate
```

### 3. Install Required Packages  
```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration  

### 1. Obtain a TMDB API Key  
- Register at [TMDB API Settings](https://www.themoviedb.org/settings/api)  
- Generate an API key

### 2. Create a `.env` File  
In the root of the project, create a `.env` file and add the following:  
```env
TMDB_API_KEY=your_api_key_here
```

---

## ▶️ Running the Analysis  

### Option 1: Run in Jupyter Notebook  
```bash
jupyter notebook
```
- Open `movie_analysis.ipynb`  
- Run all cells sequentially  

### Option 2: Run as Python Script  
```bash
python main.py
```

---

## 🧱 Project Structure  
```
tmdb-movie-analysis/
├── data/
│   ├── raw/                # Raw JSON responses from API
│   └── processed/          # Cleaned CSV files
├── notebooks/
│   └── movie_analysis.ipynb
├── scripts/
│   ├── data_fetch.py       # API data collection
│   ├── data_clean.py       # Data cleaning and processing
│   ├── analysis.py         # Analytical functions
│   └── visualization.py    # Plot generation
├── reports/
│   ├── figures/            # Output charts and graphs
│   └── analysis_report.pdf # Summary of key findings
├── .env.example            # Example environment config
├── requirements.txt        # Project dependencies
├── main.py                 # Main execution script
└── README.md               # Project documentation
```

---

## ✨ Key Features  

- ✅ Fetches movie data from TMDB API  
- 🧹 Cleans and preprocesses raw JSON data  
- 📊 Performs financial and ratings analysis  
- 📈 Generates insightful visualizations:
  - Revenue vs Budget scatter plots  
  - ROI by genre boxplots  
  - Yearly film trend lines  
  - Popularity vs Rating correlations  

---

## 📤 Outputs  

Running the project will generate:

### Processed Data  
Located in `data/processed/`:
- `movies_clean.csv` – Cleaned dataset  
- `franchise_stats.csv` – Franchise performance metrics  

### Visualizations  
Located in `reports/figures/`:
- Revenue vs Budget plots  
- Genre ROI distributions  
- Yearly trend charts  
- Popularity vs Rating plots  

### Reports  
- `analysis_report.pdf` – Summary of findings  

---

## 🧰 Troubleshooting  

| Issue                | Cause & Solution                                                   |
|---------------------|---------------------------------------------------------------------|
| **API Limit Errors**     | TMDB limits ~40 requests per 10 seconds. Add delays or request higher rate limits. |
| **Missing Data**        | Some movies lack financials. The script automatically handles missing values.        |
| **Authentication Errors** | Ensure `.env` contains a valid API key and has the required permissions.            |

---

## 🤝 Contributing  

Contributions are welcome! To contribute:

1. Fork the repository  
2. Create a new feature branch  
3. Commit your changes  
4. Push to your fork  
5. Open a pull request  

---

## 📄 License  

This project is licensed under the [MIT License](LICENSE).
