from pathlib import Path
from typing import Dict, List

import pandas as pd
from google_play_scraper import Sort, reviews


def fetch_reviews_for_app(
    app_id: str,
    bank_name: str,
    min_reviews: int = 400,
    source: str = "Google Play",
) -> List[Dict]:
    """Fetch reviews for a single Google Play app package."""
    reviews_data: List[Dict] = []
    continuation_token = None

    while len(reviews_data) < min_reviews:
        count = min(200, min_reviews - len(reviews_data))
        batch, continuation_token = reviews(
            app_id,
            lang="en",
            country="us",
            sort=Sort.NEWEST,
            count=count,
            continuation_token=continuation_token,
        )

        if not batch:
            break

        for item in batch:
            reviews_data.append(
                {
                    "review_id": item.get("reviewId") or item.get("id"),
                    "review": item.get("content") or item.get("review") or "",
                    "rating": item.get("score") or item.get("rating"),
                    "date": item.get("at"),
                    "bank": bank_name,
                    "source": source,
                }
            )

        if continuation_token is None:
            break

    return reviews_data


def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw review data and normalize it for analysis."""
    df = df.copy()
    df["review"] = df["review"].astype(str).str.strip()
    df.loc[df["review"] == "", "review"] = pd.NA
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    initial_count = len(df)
    df = df.dropna(subset=["review", "rating"])
    missing_text_rating = initial_count - len(df)

    if "review_id" in df.columns:
        df = df.drop_duplicates(subset=["review_id"])
    else:
        df = df.drop_duplicates(subset=["review", "rating", "date", "bank"])

    date_series = pd.to_datetime(df["date"], errors="coerce")
    missing_dates = date_series.isna() & df["date"].notna()
    if missing_dates.any():
        date_series.loc[missing_dates] = pd.to_datetime(
            df.loc[missing_dates, "date"],
            errors="coerce",
            format="%Y/%m/%d",
        )

    df["date"] = date_series.dt.strftime("%Y-%m-%d")
    df = df.dropna(subset=["date"])

    cleaned_df = df[["review", "rating", "date", "bank", "source"]].reset_index(drop=True)
    cleaned_count = len(cleaned_df)

    print(f"Raw records: {initial_count}")
    print(f"Dropped missing review/text or rating: {missing_text_rating}")
    print(f"Final cleaned records: {cleaned_count}")

    return cleaned_df


def save_clean_csv(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def build_review_dataset(
    bank_apps: Dict[str, str],
    output_file: Path,
    min_reviews_per_bank: int = 400,
) -> pd.DataFrame:
    all_reviews = []

    for bank_name, app_id in bank_apps.items():
        print(f"Fetching reviews for {bank_name}: {app_id}")
        bank_reviews = fetch_reviews_for_app(app_id, bank_name, min_reviews=min_reviews_per_bank)
        print(f"Collected {len(bank_reviews)} reviews for {bank_name}")
        all_reviews.extend(bank_reviews)

    raw_df = pd.DataFrame(all_reviews)
    cleaned_df = clean_reviews(raw_df)
    save_clean_csv(cleaned_df, output_file)

    return cleaned_df
