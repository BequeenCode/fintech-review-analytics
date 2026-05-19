# Interim Report: Fintech Review Analytics

## 1. Scraping Methodology and Data Quality Summary
Data collection was performed using the `google-play-scraper` Python package. We successfully extracted reviews for three prominent banks: **Commercial Bank of Ethiopia (CBE)**, **Bank of Abyssinia**, and **Dashen Bank**. 

**Data Quality:**
- Over 400 reviews were scraped per bank, totaling roughly 1,200 reviews.
- Missing text and rating fields were cleaned by dropping the incomplete rows.
- The date fields were normalized to `YYYY-MM-DD` format.
- Less than 5% of the data was missing, ensuring a robust dataset for analysis.

## 2. Early Sentiment Findings
Using a pre-trained transformer model (`distilbert-base-uncased-finetuned-sst-2-english`), we extracted sentiment scores for the cleaned reviews.

**Key Findings:**
- **Commercial Bank of Ethiopia** has a mixed sentiment distribution, with strong opinions on both ends (highly positive and highly negative).
- **Bank of Abyssinia** and **Dashen Bank** lean towards slightly higher positive sentiment, though negative reviews still pinpoint specific pain points.
- Many negative sentiments are correlated with words like "crash", "branch", and "error".

*Refer to the visualizations generated in the `notebooks/` directory for visual representations (e.g., `sentiment_by_bank.png`).*

## 3. Blockers Encountered and Plan for Final Submission
**Blockers:**
- The Google Play scraper occasionally rate-limits requests if run too frequently. This was mitigated by introducing slight delays between requests and batching them.
- Transformers token limit (512 tokens) caused exceptions on very long reviews. This was resolved by truncating reviews to 512 characters before passing them to the pipeline.

**Plan for Final Submission:**
- **Thematic Analysis**: Proceed to extract n-grams and group keywords into 3-5 distinct themes per bank.
- **Database Architecture**: Stand up a PostgreSQL instance, build relational tables (`banks` and `reviews`), and insert the fully processed dataset.
- **Final Report**: Synthesize sentiment and thematic findings into actionable business insights, detailing drivers and pain points, wrapped in a comprehensive Medium-style blog post.
