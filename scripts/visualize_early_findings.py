import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_sentiment_chart():
    # Load the data you generated in Task 2
    try:
        df = pd.read_csv('data/raw/processed_reviews.csv')
    except FileNotFoundError:
        print("Could not find processed_reviews.csv. Make sure you ran Task 2 first!")
        return

    # Set up the visual style
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")

    # Create a bar chart showing positive vs negative sentiments per bank
    # Adding NEUTRAL in case the model outputted any
    palette_colors = {'POSITIVE': '#4CAF50', 'NEGATIVE': '#F44336', 'NEUTRAL': '#9E9E9E'}
    
    sns.countplot(
        data=df, 
        x='bank', 
        hue='sentiment_label', 
        palette=palette_colors
    )
    
    # Add titles and labels
    plt.title('Early Sentiment Distribution by Bank', fontsize=16, fontweight='bold')
    plt.xlabel('Bank', fontsize=12)
    plt.ylabel('Number of Reviews', fontsize=12)
    plt.legend(title='Sentiment')
    plt.tight_layout()

    # Make sure the notebooks folder exists, then save the image there
    os.makedirs('notebooks', exist_ok=True)
    save_path = 'notebooks/sentiment_distribution.png'
    plt.savefig(save_path, dpi=300)
    
    print(f"✅ Success! Your chart has been saved to: {save_path}")

if __name__ == "__main__":
    create_sentiment_chart()