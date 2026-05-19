import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_visualizations():
    print("Generating final visualizations...")
    data_path = 'data/raw/processed_reviews.csv'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return
        
    df = pd.read_csv(data_path)
    
    # Ensure notebooks folder exists
    os.makedirs('notebooks', exist_ok=True)
    sns.set_theme(style="whitegrid")

    # 1. Sentiment distribution by bank
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='bank', hue='sentiment_label', palette={'POSITIVE': '#4CAF50', 'NEGATIVE': '#F44336', 'NEUTRAL': '#9E9E9E'})
    plt.title('Sentiment Distribution by Bank', fontsize=16)
    plt.xlabel('Bank')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('notebooks/sentiment_by_bank.png', dpi=300)
    plt.close()

    # 2. Rating distribution per bank
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='bank', y='rating', palette='Set2')
    plt.title('Rating Distribution per Bank', fontsize=16)
    plt.xlabel('Bank')
    plt.ylabel('Rating (1-5)')
    plt.tight_layout()
    plt.savefig('notebooks/rating_distribution.png', dpi=300)
    plt.close()

    # 3. Theme frequency per bank
    theme_counts = df.groupby(['bank', 'identified_theme']).size().reset_index(name='count')
    plt.figure(figsize=(14, 8))
    sns.barplot(data=theme_counts, y='identified_theme', x='count', hue='bank', palette='pastel')
    plt.title('Theme Frequency by Bank', fontsize=16)
    plt.xlabel('Number of Reviews')
    plt.ylabel('Identified Theme')
    plt.tight_layout()
    plt.savefig('notebooks/theme_frequency.png', dpi=300)
    plt.close()

    # 4. Average Sentiment Score over time (Monthly)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df['month_year'] = df['date'].dt.to_period('M')
    
    # Convert POSITIVE/NEGATIVE to numeric for trend (POSITIVE=1, NEGATIVE=-1, NEUTRAL=0)
    sentiment_map = {'POSITIVE': 1, 'NEUTRAL': 0, 'NEGATIVE': -1}
    df['sentiment_numeric'] = df['sentiment_label'].map(sentiment_map)
    
    monthly_sentiment = df.groupby(['month_year', 'bank'])['sentiment_numeric'].mean().reset_index()
    monthly_sentiment['month_year'] = monthly_sentiment['month_year'].astype(str)
    
    # Filter out months with too few data points or just plot the last 12 months for clarity
    recent_months = monthly_sentiment['month_year'].unique()[-12:]
    recent_data = monthly_sentiment[monthly_sentiment['month_year'].isin(recent_months)]
    
    plt.figure(figsize=(14, 6))
    sns.lineplot(data=recent_data, x='month_year', y='sentiment_numeric', hue='bank', marker='o')
    plt.title('Sentiment Trend Over Time (Recent 12 Months)', fontsize=16)
    plt.xlabel('Month')
    plt.ylabel('Average Sentiment (-1 to 1)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('notebooks/sentiment_trend.png', dpi=300)
    plt.close()

    print("All visualizations generated and saved in the 'notebooks' folder.")

if __name__ == "__main__":
    create_visualizations()
