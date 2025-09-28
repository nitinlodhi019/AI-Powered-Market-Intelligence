# src/llm_infer.py

import os
from groq import Groq

# --- API Client Setup ---
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    print("Error: GROQ_API_KEY environment variable not set.")
    print("Please set it before running the script.")
    client = None
# -------------------------

def generate_insight(prompt_text: str) -> str:
    """
    Generates an insight using the Groq API.
    """
    if not client:
        return "API client not initialized. Please check your API key."

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_text,
                }
            ],
            # 👇 This is now updated with the correct production model ID
            model="llama-3.1-8b-instant",
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred while calling the Groq API: {e}")
        return "Failed to generate insight due to an API error."

# ... (rest of the file remains the same) ...
if __name__ == "__main__":
    if "GROQ_API_KEY" not in os.environ:
        print("Please set your GROQ_API_KEY environment variable to test.")
    else:
        sample_prompt = """
        Analyze the following data for the app 'SocialConnect' and provide one key marketing insight.
        - Category: Social Networking
        - Rating: 4.1
        - Reviews: 250,000
        - Installs: 10,000,000+
        Based on this, what is a weakness to address?
        Insight:
        """
        print("\n--- Generating Sample Insight via Groq API ---")
        insight = generate_insight(sample_prompt)
        print(f"\nGenerated Insight:\n{insight}")