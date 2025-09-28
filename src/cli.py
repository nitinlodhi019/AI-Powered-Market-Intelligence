# src/cli.py

import json
import argparse

INSIGHTS_JSON_PATH = "outputs/insights.json"


def search_insights(query):
    """
    Loads insights and searches for an app name matching the query.
    """
    try:
        with open(INSIGHTS_JSON_PATH, 'r', encoding='utf-8') as f:
            insights = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find '{INSIGHTS_JSON_PATH}'.")
        print("Please run the main pipeline first to generate insights.")
        return

    # A simple case-insensitive search
    results = [
        insight for insight in insights
        if query.lower() in insight.get("app_name", "").lower()
    ]

    if not results:
        print(f"No insights found for an app name containing '{query}'.")
        return

    print(f"\nFound {len(results)} match(es) for '{query}':")
    print("-" * 40)

    for result in results:
        print(f"App Name: {result.get('app_name')}\n")
        print(f"Insight:\n{result.get('insight')}\n")
        print("-" * 40)


if __name__ == "__main__":
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(
        description="Search for AI-generated market intelligence insights for a specific app."
    )
    parser.add_argument(
        "-q", "--query",
        type=str,
        required=True,
        help="The name (or part of the name) of the app to search for."
    )

    args = parser.parse_args()

    search_insights(args.query)