#  Create Ranking Function
def rank_movies(df, metric, ascending=False, min_budget=None, min_votes=None):
    """Rank movies based on specified metric with optional filters"""
    df_filtered = df.copy()
    
    if min_budget is not None:
        df_filtered = df_filtered[df_filtered['budget_musd'] >= min_budget]
    
    if min_votes is not None:
        df_filtered = df_filtered[df_filtered['vote_count'] >= min_votes]
    
    if metric == 'profit':
        df_filtered['profit'] = df_filtered['revenue_musd'] - df_filtered['budget_musd']
        metric_col = 'profit'
    elif metric == 'roi':
        df_filtered['roi'] = df_filtered['revenue_musd'] / df_filtered['budget_musd']
        metric_col = 'roi'
    else:
        metric_col = metric
    
    return df_filtered.sort_values(metric_col, ascending=ascending)[['title', metric_col]]

    #  Perform Rankings

# Highest Revenue
top_revenue = rank_movies(movies_df, 'revenue_musd')

# Highest Budget
top_budget = rank_movies(movies_df, 'budget_musd')

# Highest Profit
top_profit = rank_movies(movies_df, 'profit')

# Lowest Profit
bottom_profit = rank_movies(movies_df, 'profit', ascending=True)

# Highest ROI (Budget ≥ 10M)
top_roi = rank_movies(movies_df, 'roi', min_budget=10)

# Lowest ROI (Budget ≥ 10M)
bottom_roi = rank_movies(movies_df, 'roi', ascending=True, min_budget=10)

# Most Voted
most_voted = rank_movies(movies_df, 'vote_count')

# Highest Rated (≥10 votes)
top_rated = rank_movies(movies_df, 'vote_average', min_votes=10)

# Lowest Rated (≥10 votes)
bottom_rated = rank_movies(movies_df, 'vote_average', ascending=True, min_votes=10)

# Most Popular
most_popular = rank_movies(movies_df, 'popularity')

# Advanced Filtering

# Search 1: Best-rated Science Fiction Action movies starring Bruce Willis
scifi_action = movies_df[
    movies_df['genres'].str.contains('Science Fiction|Action', na=False)
]

bruce_willis_movies = scifi_action[
    scifi_action['overview'].str.contains('Bruce Willis', case=False, na=False) |
    scifi_action['tagline'].str.contains('Bruce Willis', case=False, na=False)
].sort_values('vote_average', ascending=False)

# Search 2: Movies starring Uma Thurman, directed by Quentin Tarantino
uma_tarantino_movies = movies_df[
    (movies_df['director'] == 'Quentin Tarantino') & 
    (
        movies_df['overview'].str.contains('Uma Thurman', case=False, na=False) |
        movies_df['tagline'].str.contains('Uma Thurman', case=False, na=False)
    )
].sort_values('runtime')


# Franchise vs Standalone Comparison

# Add franchise flag
movies_df['is_franchise'] = ~movies_df['belongs_to_collection'].isna()

# Compare metrics
franchise_stats = movies_df.groupby('is_franchise').agg({
    'revenue_musd': ['mean', 'median'],
    'budget_musd': 'mean',
    'popularity': 'mean',
    'vote_average': 'mean'
}).reset_index()

# Calculate ROI for franchises
franchise_movies = movies_df[movies_df['is_franchise']]
franchise_movies['roi'] = franchise_movies['revenue_musd'] / franchise_movies['budget_musd']
franchise_roi = franchise_movies.groupby('belongs_to_collection')['roi'].median().sort_values(ascending=False)


# Most Successful Franchises

franchise_performance = movies_df.groupby('belongs_to_collection').agg({
    'title': 'count',
    'budget_musd': ['sum', 'mean'],
    'revenue_musd': ['sum', 'mean'],
    'vote_average': 'mean'
}).sort_values(('revenue_musd', 'sum'), ascending=False)

franchise_performance.columns = ['num_movies', 'total_budget', 'mean_budget', 
                                'total_revenue', 'mean_revenue', 'mean_rating']


# Most Successful Directors

director_stats = movies_df.groupby('director').agg({
    'title': 'count',
    'revenue_musd': 'sum',
    'vote_average': 'mean'
}).sort_values('revenue_musd', ascending=False)

director_stats.columns = ['num_movies', 'total_revenue', 'mean_rating']