import pandas as pd
from sqlalchemy import create_engine, text
import os

def insert_data_to_db():
    print("Starting database insertion process...")
    # Default local postgres connection string
    # Format: postgresql://username:password@host:port/database_name
    db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/bank_reviews')
    
    try:
        engine = create_engine(db_url)
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Successfully connected to the database.")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print("\nPlease ensure PostgreSQL is installed, running, and the database 'bank_reviews' exists.")
        print("You may need to update the DATABASE_URL environment variable.")
        return

    # Load the processed reviews
    data_path = 'data/raw/processed_reviews.csv'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Please run Task 2 first.")
        return
        
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} reviews from {data_path}")
    
    # We need to populate the 'banks' table first
    unique_banks = df['bank'].unique()
    bank_records = [{'bank_name': bank, 'app_name': f"{bank} App"} for bank in unique_banks]
    banks_df = pd.DataFrame(bank_records)
    
    # Insert banks
    try:
        banks_df.to_sql('banks', engine, if_exists='append', index=False)
        print("Successfully inserted banks metadata.")
    except Exception as e:
        print(f"Warning/Error inserting banks (might already exist): {e}")

    # Fetch bank_ids to map to reviews
    with engine.connect() as conn:
        result = conn.execute(text("SELECT bank_id, bank_name FROM banks"))
        bank_mapping = {row[1]: row[0] for row in result}
        
    print(f"Bank mapping retrieved: {bank_mapping}")
    
    # Prepare reviews dataframe for insertion
    reviews_df = df.copy()
    # Map bank names to bank_ids
    reviews_df['bank_id'] = reviews_df['bank'].map(bank_mapping)
    
    # Select and rename columns to match schema
    # Schema: review_id, bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, identified_theme, source
    columns_to_keep = ['review_id', 'bank_id', 'review_text', 'rating', 'date', 'sentiment_label', 'sentiment_score', 'identified_theme', 'source']
    reviews_db_df = reviews_df[columns_to_keep].rename(columns={'date': 'review_date'})
    
    # Insert reviews
    try:
        reviews_db_df.to_sql('reviews', engine, if_exists='append', index=False)
        print(f"Successfully inserted {len(reviews_db_df)} reviews.")
    except Exception as e:
        print(f"Error inserting reviews: {e}")
        return
        
    # Run verification queries
    print("\n--- Verification Queries ---")
    with engine.connect() as conn:
        # Count reviews per bank
        count_res = conn.execute(text("""
            SELECT b.bank_name, COUNT(r.review_id) 
            FROM banks b 
            LEFT JOIN reviews r ON b.bank_id = r.bank_id 
            GROUP BY b.bank_name
        """))
        print("\nReviews per bank:")
        for row in count_res:
            print(f"  {row[0]}: {row[1]}")
            
        # Average rating per bank
        avg_res = conn.execute(text("""
            SELECT b.bank_name, AVG(r.rating) 
            FROM banks b 
            LEFT JOIN reviews r ON b.bank_id = r.bank_id 
            GROUP BY b.bank_name
        """))
        print("\nAverage rating per bank:")
        for row in avg_res:
            print(f"  {row[0]}: {float(row[1] or 0):.2f}")
            
        # Check for nulls in key columns
        null_res = conn.execute(text("""
            SELECT 
                COUNT(*) FILTER (WHERE review_text IS NULL) as null_texts,
                COUNT(*) FILTER (WHERE rating IS NULL) as null_ratings
            FROM reviews
        """))
        nulls = null_res.fetchone()
        print(f"\nNull checks:\n  Null review texts: {nulls[0]}\n  Null ratings: {nulls[1]}")

if __name__ == "__main__":
    insert_data_to_db()
