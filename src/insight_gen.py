# src/insight_gen.py

import pandas as pd
from .llm_infer import generate_insight


def calculate_confidence_score(row):
    """
    Calculates a confidence score based on the richness of the input data.
    """
    score = 0.6  # Start with a base score

    # Add points if the app is on both platforms
    if row.get('platform') == 'Both':
        score += 0.15

    # Add points for a high number of Google Play reviews (more reliable data)
    try:
        if int(row.get('google_play_reviews', 0)) > 10000:
            score += 0.1
    except (ValueError, TypeError):
        pass  # Ignore if review count is not a valid number

    # Add points for a high Apple App Store rating
    try:
        if float(row.get('apple_app_store_rating', 0)) >= 4.0:
            score += 0.15
    except (ValueError, TypeError):
        pass  # Ignore if rating is not a valid number

    # Ensure the score does not exceed 1.0
    return min(score, 1.0)


def create_insights_from_data(dataframe):
    """
    Iterates through a DataFrame and generates insights for each app.
    """
    insights_list = []

    for index, row in dataframe.iterrows():
        prompt = f"""
        You are a market analyst. Based on the following combined data for the app '{row['app_name']}', generate one short, actionable marketing insight.

        - Google Play Rating: {row.get('google_play_rating', 'N/A')}
        - Google Play Reviews: {row.get('google_play_reviews', 'N/A')}
        - Google Play Installs: {row.get('google_play_installs', 'N/A')}
        - Apple App Store Rating: {row.get('apple_app_store_rating', 'N/A')}
        - Platform Availability: {row.get('platform', 'N/A')}

        Actionable Insight:
        """

        print(f"\nGenerating insight for '{row['app_name']}'...")
        generated_text = generate_insight(prompt)

        # --- THIS IS THE UPDATED PART ---
        # Calculate a dynamic confidence score instead of using a placeholder
        confidence = calculate_confidence_score(row)
        # --------------------------------

        insight_data = {
            "app_name": row['app_name'],
            "insight": generated_text,
            "confidence_score": round(confidence, 2)  # Round to 2 decimal places
        }
        insights_list.append(insight_data)
        print(f"Insight received with confidence score: {confidence:.2f}")

    return insights_list