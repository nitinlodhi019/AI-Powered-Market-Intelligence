# run_phase5.py

import pandas as pd
import os
from src.llm_infer import generate_insight  # Re-using our LLM function

# --- File Paths ---
D2C_DATA_PATH = "data/Kasparro_Phase5_D2C_Synthetic_Dataset.xlsx"
OUTPUT_DIR = "outputs"


def main():
    """
    Performs the full Phase 5 analysis: calculates metrics,
    derives insights, and generates creative content.
    """
    print("--- Starting Phase 5: D2C Market Intelligence ---")

    # 1. Load the D2C dataset
    try:
        df = pd.read_excel(D2C_DATA_PATH)
    except FileNotFoundError:
        print(f"Error: D2C data not found at '{D2C_DATA_PATH}'")
        return

    print("D2C data loaded successfully.")

    # 2. Calculate Key Metrics (CAC and ROAS)
    # CAC = Spend / Number of Customers (first_purchase)
    # ROAS = Revenue / Spend
    # We add a small number to the denominator to avoid division by zero
    df['cac'] = df['spend_usd'] / (df['first_purchase'] + 0.01)
    df['roas'] = df['revenue_usd'] / (df['spend_usd'] + 0.01)

    print("Calculated CAC and ROAS for all campaigns.")

    # 3. Find the best campaign to analyze (highest ROAS)
    best_campaign = df.loc[df['roas'].idxmax()]

    print(f"\n--- Analyzing Best Performing Campaign: {best_campaign['campaign_id']} ---")
    print(f"Channel: {best_campaign['channel']}")
    print(f"ROAS: {best_campaign['roas']:.2f}x")
    print(f"CAC: ${best_campaign['cac']:.2f}")

    # 4. Generate a strategic funnel insight for this campaign
    funnel_prompt = f"""
    Analyze the following D2C campaign data and provide a key strategic insight about its marketing funnel performance.

    - Campaign ID: {best_campaign['campaign_id']}
    - Channel: {best_campaign['channel']}
    - Spend: ${best_campaign['spend_usd']:.2f}
    - Clicks: {best_campaign['clicks']}
    - Installs: {best_campaign['installs']}
    - First-time Purchases: {best_campaign['first_purchase']}
    - Revenue: ${best_campaign['revenue_usd']:.2f}
    - Calculated ROAS (Return on Ad Spend): {best_campaign['roas']:.2f}x
    - Calculated CAC (Customer Acquisition Cost): ${best_campaign['cac']:.2f}

    Based on this, what is the single most important insight for a marketing manager?
    Strategic Insight:
    """

    print("\n--- Generating Strategic Insight... ---")
    strategic_insight = generate_insight(funnel_prompt)
    print("Insight Received:")
    print(strategic_insight)

    # 5. Generate a creative output based on the insight
    creative_prompt = f"""
    Based on the following strategic insight: '{strategic_insight}'

    Write one compelling and high-energy ad headline for a new campaign on the same channel ({best_campaign['channel']}).
    Ad Headline:
    """

    print("\n--- Generating Creative Ad Headline... ---")
    ad_headline = generate_insight(creative_prompt)
    print("Ad Headline Received:")
    print(ad_headline)

    print("\n--- Phase 5 Finished ---")


if __name__ == "__main__":
    if "GROQ_API_KEY" not in os.environ:
        print("Error: Please set your GROQ_API_KEY environment variable.")
    else:
        run_d2c_analysis()