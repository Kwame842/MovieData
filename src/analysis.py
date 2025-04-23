from pyspark.sql import functions as F
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def analyze_movies(movies_df):
    """Perform movie analysis and return results dictionary"""
    # Calculate additional metrics
    movies_df = movies_df.withColumn("profit_musd", F.col("revenue_musd") - F.col("budget_musd")) \
                        .withColumn("roi", F.col("revenue_musd") / F.col("budget_musd"))
    
    # Define analysis functions
    def get_top_n(df, metric, n=5, min_budget=None, min_votes=None):
        filtered = df
        if min_budget:
            filtered = filtered.filter(F.col("budget_musd") >= min_budget)
        if min_votes:
            filtered = filtered.filter(F.col("vote_count") >= min_votes)
        return filtered.orderBy(F.col(metric).desc()).limit(n).toPandas()
    
    # Perform analyses
    results = {
        'top_revenue': get_top_n(movies_df, "revenue_musd"),
        'top_profit': get_top_n(movies_df, "profit_musd"),
        'top_roi': get_top_n(movies_df, "roi", min_budget=10),
        'top_rated': get_top_n(movies_df, "vote_average", min_votes=10),
        'franchise_vs_standalone': movies_df.groupBy(
            F.col("belongs_to_collection").isNotNull().alias("is_franchise")
        ).agg(
            F.avg("revenue_musd").alias("avg_revenue"),
            F.expr("percentile_approx(roi, 0.5)").alias("median_roi"),
            F.avg("budget_musd").alias("avg_budget"),
            F.avg("popularity").alias("avg_popularity"),
            F.avg("vote_average").alias("avg_rating")
        ).orderBy("is_franchise").toPandas()
    }
    
    return results

def visualize_results(results):
    """Create visualizations from analysis results"""
    # Set style
    sns.set_style("whitegrid")
    plt.figure(figsize=(15, 10))
    
    # 1. Top Revenue Movies
    plt.subplot(2, 2, 1)
    sns.barplot(data=results['top_revenue'], x="revenue_musd", y="title")
    plt.title("Top 5 Movies by Revenue")
    plt.xlabel("Revenue ($M)")
    plt.ylabel("")
    
    # 2. Top Profit Movies
    plt.subplot(2, 2, 2)
    sns.barplot(data=results['top_profit'], x="profit_musd", y="title")
    plt.title("Top 5 Movies by Profit")
    plt.xlabel("Profit ($M)")
    plt.ylabel("")
    
    # 3. Franchise vs Standalone Comparison
    plt.subplot(2, 2, 3)
    sns.barplot(
        data=results['franchise_vs_standalone'], 
        x="is_franchise", 
        y="avg_revenue"
    )
    plt.title("Average Revenue: Franchise vs Standalone")
    plt.xlabel("Is Franchise?")
    plt.ylabel("Average Revenue ($M)")
    plt.xticks([0, 1], ["Standalone", "Franchise"])
    
    # 4. Top Rated Movies
    plt.subplot(2, 2, 4)
    sns.barplot(data=results['top_rated'], x="vote_average", y="title")
    plt.title("Top 5 Rated Movies (min 10 votes)")
    plt.xlabel("Average Rating")
    plt.ylabel("")
    
    plt.tight_layout()
    plt.show()
    
    # Additional ROI by Genre analysis
    if 'top_roi' in results and not results['top_roi'].empty:
        plt.figure(figsize=(12, 6))
        results['top_roi']['main_genre'] = results['top_roi']['genres'].str.split('|').str[0]
        sns.boxplot(data=results['top_roi'], x="main_genre", y="roi")
        plt.title("ROI Distribution by Genre (Budget ≥ $10M)")
        plt.xticks(rotation=45)
        plt.ylabel("ROI (Revenue/Budget)")
        plt.show()