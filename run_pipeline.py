# run_pipeline.py

import pandas as pd
import json
import os
import time
from src.ingest import search_apple_app
from src.unify import unify_app_data
from src.insight_gen import create_insights_from_data

# --- File Paths ---
GOOGLE_DATA_PATH = "data/googleplaystore_cleaned.csv"
COMBINED_DATA_PATH = "outputs/combined_apps.csv"
INSIGHTS_JSON_PATH = "outputs/insights.json"
OUTPUT_DIR = "outputs"


def main():
    """Main function to execute the full data pipeline."""
    print("--- Starting Full AI Market Intelligence Pipeline ---")

    # 1. Load the base Google Play dataset
    google_df = pd.read_csv(GOOGLE_DATA_PATH)
    print(f"Loaded {len(google_df)} records from Google Play dataset.")

    # 2. Ingest & Unify Data
    all_unified_data = []
    print("\n--- Ingesting from App Store and Unifying Data ---")
    # We'll process the first 5 apps to run quickly. Change .head(5) to process all.
    for index, row in google_df.head(5).iterrows():
        app_name = row['App']

        # Ingest: Fetch data from Apple App Store
        apple_data = search_apple_app(app_name)

        # Unify: Combine Google and Apple data
        unified_record = unify_app_data(row, apple_data)
        all_unified_data.append(unified_record)

        # Add a small delay to respect API rate limits
        time.sleep(1)

        # Create a new DataFrame with the combined data
    combined_df = pd.DataFrame(all_unified_data)

    # 3. Save the combined dataset
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    combined_df.to_csv(COMBINED_DATA_PATH, index=False)
    print(f"\nSuccessfully saved combined data for {len(combined_df)} apps to '{COMBINED_DATA_PATH}'.")

    # 4. Generate Insights based on the NEW combined data
    print("\n--- Generating AI-Powered Insights from Combined Data ---")
    # Note: You might want to update your prompt in insight_gen.py to use the new fields
    insights_data = create_insights_from_data(combined_df)

    # 5. Save the insights
    with open(INSIGHTS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(insights_data, f, indent=4)
    print(f"Insights saved to '{INSIGHTS_JSON_PATH}'.")
    print("\n--- Pipeline Finished ---")


if __name__ == "__main__":
    # Make sure both API keys are set before running
    if "RAPIDAPI_KEY" not in os.environ or "GROQ_API_KEY" not in os.environ:
        print("Error: Please set both RAPIDAPI_KEY and GROQ_API_KEY environment variables.")
    else:
        run_app_analysis()