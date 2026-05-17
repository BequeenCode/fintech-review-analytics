from pathlib import Path

from src.sentiment_thematic import (
    build_sentiment_theme_dataset,
    summarize_sentiment_by_bank_rating,
    summarize_themes,
)


def main() -> None:
    input_path = Path("data/reviews_cleaned.csv")
    output_path = Path("data/task2_sentiment_thematic.csv")

    if not input_path.exists():
        print(f"Missing input dataset: {input_path}")
        print("Run Task 1 first to generate the cleaned review CSV.")
        return

    df = build_sentiment_theme_dataset(input_path, output_path, min_reviews=400)
    print(f"Saved sentiment/theme dataset to {output_path}")

    sentiment_summary = summarize_sentiment_by_bank_rating(df)
    theme_summary = summarize_themes(df)
    print("\nSentiment summary by bank and star rating:")
    print(sentiment_summary.to_string(index=False))
    print("\nTop themes by bank:")
    print(theme_summary.groupby("bank").head(5).to_string(index=False))

    notes = (
        "Tool selection rationale: using VADER as a lightweight, production-ready "
        "baseline for sentiment with quick deployment. Transformer-based "
        "classification (distilbert-base-uncased-finetuned-sst-2-english) can be "
        "added later for comparison once model inference is configured."
    )
    print("\n", notes)


if __name__ == "__main__":
    main()
