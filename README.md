# Fintech Review Analytics

This repository contains the Task 1 implementation for scraping and preprocessing bank app reviews from the Google Play Store.

## Purpose

- Scrape review text, rating, date, bank/app name, and source from Google Play
- Normalize review data to an analysis-ready CSV
- Keep the dataset out of version control with `.gitignore`
- Validate the project with GitHub Actions on push to `main`

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

## Notes

- The current script uses placeholder app package IDs for three bank apps; replace `BANK_APPS` in `scripts/run_task1.py` with the exact Google Play package names for the target banks.
- The dataset is ignored via `.gitignore`, so CSV data is not committed.
- CI is configured to run `pytest` on every push to `main`.
