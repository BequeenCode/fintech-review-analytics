import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_sentiment():
    df = pd.read_csv('data/raw/sentiment_reviews.csv')
    
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='bank', hue='sentiment_label', palette={'POSITIVE': '#4CAF50', 'NEGATIVE': '#F44336'})
    
    plt.title('Early Sentiment Distribution by Bank')
    plt.xlabel('Bank')
    plt.ylabel('Number of Reviews')
    plt.legend(title='Sentiment')
    plt.tight_layout()
    plt.savefig('notebooks/sentiment_distribution.png')
    print("Saved visualization to notebooks/sentiment_distribution.png")

if __name__ == "__main__":
    visualize_sentiment()