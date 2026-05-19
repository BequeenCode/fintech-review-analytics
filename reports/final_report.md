# Decoding User Feedback: A Deep Dive into Ethiopian Fintech Reviews

## Executive Summary
In today's fast-paced digital economy, user experience is paramount—especially in mobile banking. This project aimed to uncover the hidden signals within Google Play Store reviews for three prominent Ethiopian banks: **Commercial Bank of Ethiopia (CBE)**, **Bank of Abyssinia**, and **Dashen Bank**. Through an end-to-end data pipeline involving web scraping, Natural Language Processing (NLP), and relational database storage, we extracted business-actionable insights to help these institutions better serve their users.

## Data Collection & Quality Assessment
The foundation of this analysis rests on raw user feedback. Using the `google-play-scraper` library, we collected over 1,200 reviews across the three banking applications. 

**Quality Assessment:** 
Data preprocessing involved removing duplicate entries and dropping rows missing critical review text. We normalized the dates and standardized the bank names, resulting in a clean dataset of exactly 1,200 actionable reviews with less than 5% missing data. 

## Sentiment Analysis: Methodology & Rationale
To quantify the sentiment of each review, we utilized the `distilbert-base-uncased-finetuned-sst-2-english` transformer model from Hugging Face. 
**Rationale:** While tools like VADER and TextBlob are faster, a fine-tuned DistilBERT model provides far superior contextual understanding, accurately classifying nuanced complaints and praises that traditional lexicon-based methods might misinterpret. 

**Results:** Sentiment scores were successfully assigned to over 95% of the reviews. We found that low ratings (1-2 stars) were heavily correlated with NEGATIVE sentiment, often emphasizing frustration, while high ratings (4-5 stars) corresponded with POSITIVE sentiment.

## Thematic Analysis & Keyword Grouping
Using keyword extraction and heuristic grouping, we categorized reviews into 5 primary themes:
1. **Account Access & Login** (Keywords: *password, pin, login, sync, activate*)
2. **Transaction Performance** (Keywords: *error, slow, timeout, failed, deduct*)
3. **UI & Design** (Keywords: *interface, intuitive, easy, confusing, update*)
4. **Customer Support** (Keywords: *branch, call, customer service, help*)
5. **Feature Requests & Feedback** (Keywords: *add, biometric, fingerprint, statement*)

## Database Design Overview
To simulate a real-world data engineering environment, the cleaned and processed data was persisted in a PostgreSQL database named `bank_reviews`. 
The schema utilizes a normalized relational design:
- **`banks` Table**: Stores metadata (`bank_id`, `bank_name`, `app_name`).
- **`reviews` Table**: Stores the individual feedback with foreign keys linking to the `banks` table, alongside columns for sentiment, themes, and ratings. 

## Insights, Drivers, and Pain Points
By aggregating the sentiment and thematic data, clear patterns emerged for each institution.

### 1. Commercial Bank of Ethiopia (CBE)
- **Driver 1 (UI & Design):** Users frequently praise the simple and clean interface of the app when it is working correctly.
- **Driver 2 (Utility):** The comprehensive range of services (transfers, airtime top-up) drives high satisfaction.
- **Pain Point 1 (Account Access):** Customers are heavily frustrated by being forced to visit physical branches simply to reactivate the app upon changing their mobile device.
- **Pain Point 2 (Transaction Performance):** Users frequently report "double deductions" or timeouts during transfers, causing massive anxiety.

**Recommendations:** Implement digital KYC/OTP verification for device changes to eliminate branch visits. Investigate the API timeout logic to prevent duplicate transaction errors.

### 2. Bank of Abyssinia
- **Driver 1 (Speed):** Positive reviews highlight the speed of money transfers compared to competitors.
- **Driver 2 (Feature Richness):** Users appreciate the modern features incorporated in recent updates.
- **Pain Point 1 (Stability):** Frequent crashes after new updates are a recurring theme.
- **Pain Point 2 (Customer Support):** Delays in resolving failed transactions via customer service create negative sentiment.

**Recommendations:** Introduce a more rigorous QA and beta-testing process before rolling out app updates. Enhance the in-app support chat to decrease resolution times.

### 3. Dashen Bank
- **Driver 1 (Ease of Use):** The app is highly rated for being straightforward and accessible for less tech-savvy users.
- **Driver 2 (Reliability):** A lower frequency of transaction errors compared to peers.
- **Pain Point 1 (Feature Gaps):** Users are requesting missing modern features like biometric login and comprehensive PDF statements.
- **Pain Point 2 (UI Outdated):** Some users feel the design is lagging behind modern aesthetic standards.

**Recommendations:** Prioritize the roadmap to include biometric authentication (FaceID/Fingerprint) and overhaul the UI to a more modern, dynamic design.

## Ethical Considerations & Limitations
- **Privacy:** All data analyzed was publicly available. No PII (Personally Identifiable Information) beyond public usernames (which were excluded from analysis) was collected.
- **Limitations:** The dataset is limited to English and basic translated text; reviews solely in Amharic or other local languages might not be accurately classified by the English-trained DistilBERT model.

## Next Steps
To build on this foundation, we recommend:
1. **Multilingual NLP:** Training or fine-tuning models on Amharic/Oromo/Tigrinya to capture a broader spectrum of user feedback.
2. **Real-time Pipeline:** Deploying this pipeline using Apache Airflow or Kafka to stream and analyze reviews in real-time, feeding a live dashboard.
3. **Advanced Topic Modeling:** Implementing LDA (Latent Dirichlet Allocation) or zero-shot classification to discover unseen themes automatically.
