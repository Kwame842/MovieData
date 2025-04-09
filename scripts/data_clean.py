
# Drop Irrelevant Columns
columns_to_drop = ['adult', 'imdb_id', 'original_title', 'video', 'homepage']
movies_df = movies_df.drop(columns=columns_to_drop, errors='ignore')

# Process JSON-like Columns
def extract_json_field(row, field_name, subfield='name'):
    """Extract values from JSON-like columns"""
    field_value = row[field_name]
    
    # Handle array-like input (convert to first element if array)
    if isinstance(field_value, (np.ndarray, list, pd.Series)):
        if len(field_value) == 0:
            return np.nan
        field_value = field_value[0]
    
    # Handle NaN/None cases
    if pd.isna(field_value):
        return np.nan
    
    # Handle empty string case
    if isinstance(field_value, str) and not field_value.strip():
        return np.nan
    
    # Handle empty dictionary case
    if isinstance(field_value, dict) and not field_value:
        return np.nan
    
    try:
        # Parse JSON if it's a string, otherwise use as-is
        data = json.loads(field_value) if isinstance(field_value, str) else field_value
        
        if isinstance(data, list):
            return "|".join([str(item.get(subfield, '')) for item in data if isinstance(item, dict)])
        elif isinstance(data, dict):
            return data.get(subfield, np.nan)
        return np.nan
    except (json.JSONDecodeError, TypeError, AttributeError):
        return np.nan

# Apply to JSON columns
json_columns = {
    'belongs_to_collection': 'name',
    'genres': 'name',
    'production_countries': 'name',
    'production_companies': 'name',
    'spoken_languages': 'name'
}

for col, subfield in json_columns.items():
    movies_df[col] = movies_df.apply(lambda x: extract_json_field(x, col, subfield), axis=1)

# Handle Missing and Incorrect Data
# Convert data types
movies_df['budget'] = pd.to_numeric(movies_df['budget'], errors='coerce')
movies_df['revenue'] = pd.to_numeric(movies_df['revenue'], errors='coerce')
movies_df['popularity'] = pd.to_numeric(movies_df['popularity'], errors='coerce')
movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], errors='coerce')

# Convert budget and revenue to million USD
movies_df['budget_musd'] = movies_df['budget'] / 1_000_000
movies_df['revenue_musd'] = movies_df['revenue'] / 1_000_000

# Handle zero values
for col in ['budget', 'revenue', 'runtime']:
    movies_df.loc[movies_df[col] == 0, col] = np.nan

# Handle vote data
movies_df.loc[movies_df['vote_count'] == 0, 'vote_average'] = np.nan

# Handle text placeholders
text_columns = ['overview', 'tagline']
for col in text_columns:
    movies_df.loc[movies_df[col].isin(['No Data', 'No overview', '']), col] = np.nan

# Remove duplicates and invalid entries
movies_df = movies_df.drop_duplicates(subset=['id', 'title'])
movies_df = movies_df.dropna(subset=['id', 'title'])

# First check if 'credits' column exists
if 'credits' not in movies_df.columns:
    print("Warning: 'credits' column not found in the DataFrame")
    # Create empty columns if credits doesn't exist
    movies_df['director'] = np.nan
    movies_df['cast_size'] = 0
    movies_df['crew_size'] = 0
else:
    # Define your extraction functions
    def extract_director(credits):
        """Extract director from credits data"""
        if pd.isna(credits) or credits == {}:
            return np.nan
        try:
            credits_data = json.loads(credits) if isinstance(credits, str) else credits
            for person in credits_data.get('crew', []):
                if person.get('job') == 'Director':
                    return person['name']
            return np.nan
        except:
            return np.nan

    def extract_cast_size(credits):
        """Count number of cast members"""
        if pd.isna(credits) or credits == {}:
            return 0
        try:
            credits_data = json.loads(credits) if isinstance(credits, str) else credits
            return len(credits_data.get('cast', []))
        except:
            return 0

    def extract_crew_size(credits):
        """Count number of crew members"""
        if pd.isna(credits) or credits == {}:
            return 0
        try:
            credits_data = json.loads(credits) if isinstance(credits, str) else credits
            return len(credits_data.get('crew', []))
        except:
            return 0

    # Apply the functions
    movies_df['director'] = movies_df['credits'].apply(extract_director)
    movies_df['cast_size'] = movies_df['credits'].apply(extract_cast_size)
    movies_df['crew_size'] = movies_df['credits'].apply(extract_crew_size)


    #  Finalize DataFrame Structure
final_columns = [
    'id', 'title', 'tagline', 'release_date', 'genres', 'belongs_to_collection',
    'original_language', 'budget_musd', 'revenue_musd', 'production_companies',
    'production_countries', 'vote_count', 'vote_average', 'popularity', 'runtime',
    'overview', 'spoken_languages', 'poster_path', 'cast_size', 'director', 'crew_size'
]

movies_df = movies_df[final_columns].reset_index(drop=True)


