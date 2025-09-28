# streamlit_app.py

import streamlit as st
import json
import pandas as pd
import os
from src.llm_infer import generate_insight

# --- File Paths ---
INSIGHTS_JSON_PATH = "outputs/insights.json"
D2C_DATA_PATH = "data/Kasparro_Phase5_D2C_Synthetic_Dataset.xlsx"


# --- Data Loading Functions ---
@st.cache_data
def load_app_insights():
    """Loads the app store insights data from the JSON file."""
    try:
        with open(INSIGHTS_JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


@st.cache_data
def load_d2c_data():
    """Loads and processes the D2C dataset."""
    try:
        df = pd.read_excel(D2C_DATA_PATH)
        # Calculate Key Metrics
        df['cac'] = df['spend_usd'] / (df['first_purchase'] + 0.01)
        df['roas'] = df['revenue_usd'] / (df['spend_usd'] + 0.01)
        return df
    except FileNotFoundError:
        return None


# --- App Layout ---
st.set_page_config(layout="wide")
st.title("🤖 AI-Powered Market Intelligence")

# --- Sidebar for Navigation ---
st.sidebar.title("Navigation")
analysis_choice = st.sidebar.radio(
    "Choose an analysis to view:",
    ("App Store Insights", "Phase 5: D2C Campaign Analysis")
)

st.sidebar.info(
    "This app demonstrates a full pipeline for ingesting data, generating AI insights, and presenting the results.")

# --- Main Page Content ---

if analysis_choice == "App Store Insights":
    st.header("🔍 Google Play & Apple App Store Insights")
    insights = load_app_insights()
    if insights is None:
        st.error(f"Error: Could not find '{INSIGHTS_JSON_PATH}'. Please run the 'app-analysis' phase first.")
    else:
        search_query = st.text_input("Enter an app name to search:", placeholder="e.g., 'Photo Editor'")
        if search_query:
            results = [i for i in insights if search_query.lower() in i.get("app_name", "").lower()]
            if not results:
                st.warning("No matches found.")
            else:
                for r in results:
                    st.subheader(r['app_name'])
                    st.info(r['insight'])
                    st.write(f"Confidence: {r['confidence_score']}")
        else:
            for r in insights:
                st.subheader(r['app_name'])
                st.info(r['insight'])
                st.write(f"Confidence: {r['confidence_score']}")


elif analysis_choice == "Phase 5: D2C Campaign Analysis":
    st.header("📈 D2C Marketing Funnel & Creative Generation")
    d2c_df = load_d2c_data()
    if d2c_df is None:
        st.error(f"Error: Could not find '{D2C_DATA_PATH}'.")
    else:
        st.info(
            "This page analyzes the D2C dataset, identifies the best campaign by ROAS, and uses AI to generate a strategic insight and a creative ad headline.")

        # Find the best campaign
        best_campaign = d2c_df.loc[d2c_df['roas'].idxmax()]

        st.subheader(f"🏆 Best Performing Campaign: {best_campaign['campaign_id']}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Channel", best_campaign['channel'])
        col2.metric("ROAS (Return on Ad Spend)", f"{best_campaign['roas']:.2f}x")
        col3.metric("CAC (Customer Acquisition Cost)", f"${best_campaign['cac']:.2f}")

        if st.button("Generate AI Insights for this Campaign"):
            with st.spinner("Generating strategic insight..."):
                funnel_prompt = f"""
                Analyze this D2C campaign data and provide a key strategic insight about its funnel performance.
                - Campaign ID: {best_campaign['campaign_id']}, Channel: {best_campaign['channel']}
                - ROAS: {best_campaign['roas']:.2f}x, CAC: ${best_campaign['cac']:.2f}
                Strategic Insight:
                """
                strategic_insight = generate_insight(funnel_prompt)
                st.subheader("🧠 Strategic Insight")
                st.success(strategic_insight)

            with st.spinner("Generating creative ad headline..."):
                creative_prompt = f"""
                Based on the insight: '{strategic_insight}', write one compelling ad headline for a new campaign on the {best_campaign['channel']} channel.
                Ad Headline:
                """
                ad_headline = generate_insight(creative_prompt)
                st.subheader("💡 Creative Ad Headline")
                st.success(ad_headline)