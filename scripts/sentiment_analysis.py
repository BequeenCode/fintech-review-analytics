import pandas as pd
from transformers import pipeline

def run_sentiment_analysis():
    df = pd.read_csv('data/raw/cleaned_reviews.csv')
    
    # Using the designated fine-tuned DistilBERT model
    print("Loading HuggingFace Pipeline...")
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    
    sentiments = []
    scores = []
    
    print("Classifying reviews...")
    for text in df['review']:
        try:
            # Truncate to 512 characters to prevent token limits
            result = sentiment_pipeline(str(text)[:512])[0]
            sentiments.append(result['label'])
            scores.append(result['score'])
        except Exception:
            sentiments.append('NEUTRAL')
            scores.append(0.0)
            
    df['sentiment_label'] = sentiments
    df['sentiment_score'] = scores
    
    df.to_csv('data/raw/sentiment_reviews.csv', index=False)
    print("Sentiment analysis complete. Saved to sentiment_reviews.csv")

if __name__ == "__main__":
    run_sentiment_analysis()