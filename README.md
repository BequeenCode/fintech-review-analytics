# Fintech Review Analytics

## Task 1 Implementation

Files created for Task 1:
- `src/data_pipeline.py` — scraper and preprocessing pipeline
- `scripts/run_task1.py` — run the scraper and save cleaned CSV
- `tests/test_data_pipeline.py` — validation for cleaning logic

## How to run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the scraping and preprocessing script:
   ```bash
   python scripts/run_task1.py
   ```
3. The cleaned dataset will be saved to `data/reviews_cleaned.csv`.

## Scraping Methodology & Data Quality
Data was collected using the `google-play-scraper` library. We scraped reviews from three prominent banks on the Google Play Store (Bank of Abyssinia, Commercial Bank of Ethiopia, and Dashen Bank). 
The data collected includes:
- Review text
- Rating (1-5)
- Date
- Bank Name
- Source

**Limitations:** We encountered missing values in some reviews (e.g., empty text). These rows were dropped during preprocessing. A total of ~1200 reviews were cleaned and normalized. Duplicate reviews were removed.

## Database Setup

To persistently store the processed review data, we simulate a data engineering workflow using PostgreSQL.

### Schema Overview
The database `bank_reviews` uses a relational design with two tables:

1. **`banks` Table**
   - `bank_id` (PRIMARY KEY)
   - `bank_name`
   - `app_name`

2. **`reviews` Table**
   - `review_id` (PRIMARY KEY)
   - `bank_id` (FOREIGN KEY referencing `banks`)
   - `review_text`
   - `rating`
   - `review_date`
   - `sentiment_label`
   - `sentiment_score`
   - `identified_theme`
   - `source`

### Setup Instructions
1. Install PostgreSQL on your machine.
2. Create a database named `bank_reviews`:
   ```sql
   CREATE DATABASE bank_reviews;
   ```
3. Initialize the schema using the provided `schema.sql`:
   ```bash
   psql -U postgres -d bank_reviews -f schema.sql
   ```
4. Insert the data via the python script:
   ```bash
   # Make sure to set the DATABASE_URL environment variable if using non-default credentials
   python scripts/db_insert.py
   ```
