import pandas as pd
import re
import os

# Define keyword mappings for thematic analysis
THEME_KEYWORDS = {
    "Account Access & Login": ['password', 'pin', 'login', 'sync', 'lock', 'block', 'activate', 'verification', 'auth', 'access', 'connection'],
    "Transaction Performance": ['slow', 'fast', 'error', 'double', 'network', 'timeout', 'failed', 'deduction', 'deduct', 'transfer', 'sent', 'pending', 'crash', 'bug', 'glitch'],
    "UI & Design": ['ui', 'design', 'interface', 'intuitive', 'easy', 'hard to use', 'simple', 'confusing', 'update', 'layout', 'navigate'],
    "Customer Support": ['support', 'branch', 'call', 'reply', 'answer', 'customer service', 'help', 'contact'],
    "Feature Requests & Feedback": ['add', 'feature', 'please', 'wish', 'biometric', 'fingerprint', 'statement', 'receipt', 'download']
}

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def assign_theme(text):
    cleaned = clean_text(text)
    theme_scores = {theme: 0 for theme in THEME_KEYWORDS.keys()}
    
    words = cleaned.split()
    for word in words:
        for theme, keywords in THEME_KEYWORDS.items():
            if word in keywords:
                theme_scores[theme] += 1
                
    # Also check for multi-word phrases
    for theme, keywords in THEME_KEYWORDS.items():
        for kw in keywords:
            if " " in kw and kw in cleaned:
                theme_scores[theme] += 2 # Give more weight to multi-word matches
                
    # Find the theme with the highest score
    best_theme = max(theme_scores, key=theme_scores.get)
    if theme_scores[best_theme] > 0:
        return best_theme
    return "General Feedback" # Default theme if no keywords matched

def run_thematic_analysis():
    print("Starting thematic analysis...")
    input_file = 'data/raw/sentiment_reviews.csv'
    output_file = 'data/raw/processed_reviews.csv'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Please run sentiment_analysis.py first.")
        return
        
    df = pd.read_csv(input_file)
    
    # Add a review_id if not present
    if 'review_id' not in df.columns:
        df.insert(0, 'review_id', range(1, len(df) + 1))
        
    # Assign themes
    print("Assigning themes to reviews...")
    df['identified_theme'] = df['review'].apply(assign_theme)
    
    # Ensure correct columns are present. Task wants:
    # review_id, review_text, sentiment_label, sentiment_score, identified_theme
    # Wait, they might also need the original columns (bank, rating, date) for later tasks.
    # I will rename 'review' to 'review_text' and keep other necessary columns.
    df = df.rename(columns={'review': 'review_text'})
    
    df.to_csv(output_file, index=False)
    print(f"Thematic analysis complete. Saved to {output_file}")
    
    # Print theme distribution per bank
    print("\nTheme Distribution:")
    print(df.groupby(['bank', 'identified_theme']).size().unstack(fill_value=0))

if __name__ == "__main__":
    run_thematic_analysis()
