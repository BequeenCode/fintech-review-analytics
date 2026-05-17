from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def ensure_nltk_data() -> None:
    try:
        stopwords.words("english")
        word_tokenize("test")
    except LookupError:
        nltk.download("stopwords")
        nltk.download("punkt")


def load_reviews(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    if "review_id" not in df.columns:
        df["review_id"] = df.index.astype(str)
    df = df.rename(columns={"review": "review_text"})
    return df


def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    return " ".join(word_tokenize(text.lower().replace("\n", " ").strip()))


def get_sentiment_label(score: float) -> str:
    if score >= 0.05:
        return "positive"
    if score <= -0.05:
        return "negative"
    return "neutral"


def score_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    ensure_nltk_data()
    analyzer = SentimentIntensityAnalyzer()
    df = df.copy()
    df["normalized_review"] = df["review_text"].astype(str).apply(normalize_text)

    df["sentiment_score"] = df["normalized_review"].apply(
        lambda text: analyzer.polarity_scores(text)["compound"]
    )
    df["sentiment_label"] = df["sentiment_score"].apply(get_sentiment_label)
    return df


def get_theme_keywords() -> Dict[str, List[str]]:
    return {
        "Account Access Issues": [
            "login",
            "sign in",
            "signin",
            "password",
            "locked",
            "authentication",
            "biometric",
            "face id",
            "fingerprint",
            "account locked",
        ],
        "Transaction Performance": [
            "transfer",
            "payment",
            "deposit",
            "withdraw",
            "transaction",
            "pending",
            "slow",
            "failed",
            "processing",
            "refund",
        ],
        "UI & Design": [
            "ui",
            "interface",
            "layout",
            "screen",
            "navigation",
            "button",
            "design",
            "experience",
            "menu",
            "slow app",
        ],
        "Customer Support": [
            "support",
            "help",
            "agent",
            "call",
            "chat",
            "customer service",
            "representative",
            "service",
            "support team",
        ],
        "Feature Requests": [
            "feature",
            "update",
            "notification",
            "budget",
            "alert",
            "mobile deposit",
            "bill pay",
            "statement",
            "account summary",
        ],
    }


def assign_theme(text: str, theme_keywords: Dict[str, List[str]]) -> str:
    text_lower = text.lower()
    for theme, keywords in theme_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                return theme
    return "Other"


def extract_top_keywords(
    texts: List[str],
    top_n: int = 15,
    ngram_range: tuple = (1, 2),
) -> List[str]:
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=ngram_range,
        max_features=200,
    )
    matrix = vectorizer.fit_transform(texts)
    feature_array = vectorizer.get_feature_names_out()
    tfidf_scores = matrix.sum(axis=0).A1
    top_indices = tfidf_scores.argsort()[::-1][:top_n]
    return [feature_array[i] for i in top_indices]


def build_sentiment_theme_dataset(
    input_csv: Path,
    output_csv: Path,
    min_reviews: Optional[int] = None,
) -> pd.DataFrame:
    df = load_reviews(input_csv)
    if min_reviews is not None and len(df) < min_reviews:
        print(
            f"Warning: only {len(df)} reviews available, target was {min_reviews}."
        )

    df = score_sentiment(df)
    theme_keywords = get_theme_keywords()
    df["identified_theme"] = df["review_text"].astype(str).apply(
        lambda text: assign_theme(text, theme_keywords)
    )

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df[
        ["review_id", "review_text", "sentiment_label", "sentiment_score", "identified_theme", "bank", "rating", "date", "source"]
    ].to_csv(output_csv, index=False)
    return df


def summarize_sentiment_by_bank_rating(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["bank", "rating"])["sentiment_score"]
        .mean()
        .reset_index()
        .rename(columns={"sentiment_score": "avg_sentiment_score"})
    )


def summarize_themes(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["bank", "identified_theme"])["review_id"]
        .count()
        .reset_index()
        .rename(columns={"review_id": "review_count"})
        .sort_values(["bank", "review_count"], ascending=[True, False])
    )
