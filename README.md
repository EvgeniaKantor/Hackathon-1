SynchroCosmetics

A recommendation system for beauty bloggers

Overview

SynchroCosmetics is a recommendation system designed for beauty bloggers. It leverages audience data to improve content and optimize product recommendations. By analyzing user details such as age, gender, skin type, and cosmetic preferences, it suggests the best beauty products, offering a personalized experience for followers.

Scenario

Imagine you're a beauty blogger sharing skincare insights on Instagram or Telegram. To better connect with your audience, you analyze social media insights (e.g., age, gender, location) and conduct surveys on skin type and cosmetic goals.

💡 SynchroCosmetics helps you:

✔ Identify key audience segments

✔ Recommend cosmetics based on audience preferences

✔ Create personalized content strategies for better engagement

How It Works

The system processes audience data and generates personalized product recommendations based on user attributes.

Key Components

📌 AudienceDF.ipynb – Creates realistic cosmetic customer profiles with:

Name (gender-based)

Gender distribution (80% Female, 20% Male)

Age (12-90, normally distributed, peak at 40)

Skin Type (5 categories)

Cosmetic Features (1-3 per user, age-based)

📌 PrepCosmeticDF.ipynb – Uses Kaggle data and enriches it with cosmetic features via OpenAI API.

📌 CosmeticDF.ipynb – Performs data analysis, visualization, and statistics.

📌 SynchroCosmetics.py – Implements the recommendation algorithm.
