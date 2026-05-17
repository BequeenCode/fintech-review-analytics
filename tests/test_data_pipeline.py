from pathlib import Path

import pandas as pd

from src.data_pipeline import clean_reviews


def test_clean_reviews_removes_empty_rows_and_normalizes_dates(tmp_path: Path) -> None:
    raw_data = {
        "review_id": ["1", "2", "3", "3"],
        "review": ["Great app", "", "Needs work", "Needs work"],
        "rating": [5, 4, 3, 3],
        "date": ["2024-01-01", None, "2024/02/01", "2024/02/01"],
        "bank": ["Bank A", "Bank A", "Bank B", "Bank B"],
        "source": ["Google Play", "Google Play", "Google Play", "Google Play"],
    }
    df = pd.DataFrame(raw_data)

    cleaned = clean_reviews(df)

    assert len(cleaned) == 2
    assert list(cleaned.columns) == ["review", "rating", "date", "bank", "source"]
    assert cleaned.iloc[0]["date"] == "2024-01-01"
    assert cleaned.iloc[1]["date"] == "2024-02-01"
