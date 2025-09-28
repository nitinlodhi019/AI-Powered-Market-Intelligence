# main.py

import argparse
import os
import subprocess
from run_pipeline import main as run_app_analysis
from run_phase5 import main as run_d2c_analysis


def main():
    parser = argparse.ArgumentParser(description="AI-Powered Market Intelligence Pipeline Controller.")
    parser.add_argument(
        "--phase",
        type=str,
        required=True,
        choices=['app-analysis', 'd2c'],
        help="Choose which pipeline phase to run: 'app-analysis' or 'd2c'."
    )
    args = parser.parse_args()

    if args.phase == 'app-analysis':
        print("--- LAUNCHING APP ANALYSIS PIPELINE ---")
        if "RAPIDAPI_KEY" not in os.environ or "GROQ_API_KEY" not in os.environ:
            print("\nError: Please set both RAPIDAPI_KEY and GROQ_API_KEY environment variables.")
            return
        run_app_analysis()

    elif args.phase == 'd2c':
        print("--- LAUNCHING D2C (PHASE 5) PIPELINE ---")
        if "GROQ_API_KEY" not in os.environ:
            print("\nError: Please set your GROQ_API_KEY environment variable.")
            return
        run_d2c_analysis()

    # --- This part now runs for BOTH phases ---
    print("\n--- LAUNCHING STREAMLIT WEB APP ---")
    # You can choose the default view by setting the query parameter
    # For now, it will just open the app.
    subprocess.run(["streamlit", "run", "streamlit_app.py"])


if __name__ == "__main__":
    main()