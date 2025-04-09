# Revenue vs Budget Scatter Plot

plt.figure(figsize=(10, 6))
sns.scatterplot(data=movies_df, x='budget_musd', y='revenue_musd', hue='is_franchise')
plt.title('Revenue vs Budget by Franchise Status')
plt.xlabel('Budget (Million USD)')
plt.ylabel('Revenue (Million USD)')
plt.grid(True)
plt.show()

# ROI Distribution by Genre

# Explode genres into separate rows
movies_with_genres = movies_df.assign(genres=movies_df['genres'].str.split('|')).explode('genres')

# Calculate ROI
movies_with_genres['roi'] = movies_with_genres['revenue_musd'] / movies_with_genres['budget_musd']

plt.figure(figsize=(12, 6))
sns.boxplot(data=movies_with_genres[movies_with_genres['budget_musd'] >= 10], 
            x='genres', y='roi')
plt.xticks(rotation=45)
plt.title('ROI Distribution by Genre (Budget ≥ $10M)')
plt.ylabel('ROI (Revenue/Budget)')
plt.show()


# Popularity vs Rating

plt.figure(figsize=(10, 6))
sns.scatterplot(data=movies_df, x='vote_average', y='popularity', hue='is_franchise')
plt.title('Popularity vs Rating')
plt.xlabel('Average Rating')
plt.ylabel('Popularity Score')
plt.show()

# Yearly Trends

movies_df['release_year'] = movies_df['release_date'].dt.year
yearly_stats = movies_df.groupby('release_year').agg({
    'budget_musd': 'mean',
    'revenue_musd': 'mean',
    'vote_average': 'mean'
}).reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=yearly_stats, x='release_year', y='budget_musd', label='Budget')
sns.lineplot(data=yearly_stats, x='release_year', y='revenue_musd', label='Revenue')
plt.title('Yearly Trends in Budget and Revenue')
plt.xlabel('Year')
plt.ylabel('Million USD')
plt.legend()
plt.show()

