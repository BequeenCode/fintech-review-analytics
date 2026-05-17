from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data_pipeline import build_review_dataset


BANK_APPS = {
    # Replace these sample app IDs with the actual bank apps you want to target.
    "Bank of America": "com.infonow.bofa",
    "Chase Mobile": "com.chase.sig.android",
    "Wells Fargo": "com.wf.wellsfargomobile",
}


def main() -> None:
    output_path = Path("data/reviews_cleaned.csv")
    build_review_dataset(BANK_APPS, output_path, min_reviews_per_bank=400)
    print(f"Saved cleaned dataset to {output_path}")


if __name__ == "__main__":
    main()
