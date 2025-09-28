# src/ingest.py

import requests
import json
import os

# --- API Configuration ---
API_URL = "https://appstore-scrapper-api.p.rapidapi.com/v1/app-store-api/reviews?id=364709193&sort=mostRecent&page=1&contry=us&lang=en"
API_HOST = "appstore-scrapper-api.p.rapidapi.com"
API_KEY = os.environ.get("RAPIDAPI_KEY")


# -------------------------

def search_apple_app(app_name: str, country: str = "us") -> dict:
    """
    Searches for an app on the Apple App Store using RapidAPI.
    """
    if not API_KEY:
        print("Error: RAPIDAPI_KEY environment variable not set.")
        return None

    querystring = {"term": app_name, "country": country, "limit": "1"}

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    print(f"Searching for '{app_name}' on the Apple App Store...")
    try:
        response = requests.get(API_URL, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()

        # The API returns a list of results directly
        if data:  # Check if the list is not empty
            return data[0]  # Return the first result from the list
        else:
            print(f"No Apple App Store results found for '{app_name}'.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while calling the RapidAPI: {e}")
        return None


if __name__ == '__main__':
    # This block allows you to test this file directly
    print("--- Testing RapidAPI Ingestion ---")

    # Check for the API key
    if "RAPIDAPI_KEY" not in os.environ:
        print("Error: Please set your RAPIDAPI_KEY environment variable to test.")
    else:
        test_app_name = "Instagram"
        app_details = search_apple_app(test_app_name)

        if app_details:
            print(f"\nSuccessfully fetched data for '{test_app_name}':")
            print(json.dumps(app_details, indent=2))