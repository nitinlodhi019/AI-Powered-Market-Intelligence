# AI-Powered Market Intelligence Pipeline

This project is a comprehensive data pipeline built to ingest market data from multiple sources, generate strategic insights using Large Language Models (LLMs), and present the findings through a user-friendly web interface.

## Project Demo

Here is a quick demonstration of the final Streamlit web application, showcasing both the App Store and D2C analysis phases.

*(Consider adding a GIF or a short video of your application here)*

## Features

- **Multi-Source Ingestion**: Ingests data from both static CSV files (Google Play Store) and a live external API (RapidAPI for Apple App Store).
- **Data Unification**: Combines and standardizes data from different sources into a single, clean dataset.
- **AI-Powered Insights**: Uses the Groq API with the Llama 3 model to generate actionable marketing insights.
- **D2C Funnel Analysis**: Adapts the pipeline to analyze e-commerce data, calculate key metrics like ROAS and CAC, and generate strategic and creative marketing content.
- **Dynamic Confidence Scoring**: Implements a logic-based system to score the reliability of each generated insight.
- **Interactive Web Interface**: A Streamlit application provides a user-friendly interface to view and interact with the results of both analysis phases.
- **CLI Interface**: A command-line tool is also available for querying app store insights.

## Project Structure

```
market-intel/
├── data/
│   ├── googleplaystore_cleaned.csv   # Cleaned Google Play data
│   └── d2c_data.xlsx                 # Synthetic D2C dataset
├── outputs/
│   ├── combined_apps.csv             # Unified app store data
│   └── insights.json                 # AI-generated insights for apps
├── src/
│   ├── ingest.py                     # Fetches data from RapidAPI
│   ├── unify.py                      # Merges Google and Apple data
│   ├── llm_infer.py                  # Handles all LLM API calls
│   ├── insight_gen.py                # Creates prompts and generates insights
│   ├── report_gen.py                 # Generates a markdown report
│   └── cli.py                        # Command-line interface
├── main.py                           # Main controller to run the project
├── run_pipeline.py                   # Runs the app analysis pipeline
├── run_phase5.py                     # Runs the D2C analysis pipeline
├── streamlit_app.py                  # The Streamlit web application
└── requirements.txt                  # All Python package dependencies
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd market-intel
    ```

2.  **Create and activate a virtual environment:**
    This project uses a virtual environment to manage dependencies.

    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate it (on Windows)
    .\venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Environment Variables:**
    This project requires two API keys. You must set them as environment variables in your terminal session before running the application.

    - `GROQ_API_KEY`: Your API key from [Groq](https://console.groq.com/).
    - `RAPIDAPI_KEY`: Your API key from the [App Store Scraper on RapidAPI](https://rapidapi.com/principalapis/api/app-store-scraper).

    In PowerShell, use the following commands:
    ```powershell
    $env:GROQ_API_KEY="YOUR_GROQ_API_KEY_HERE"
    $env:RAPIDAPI_KEY="YOUR_RAPIDAPI_KEY_HERE"
    ```

## How to Run

Use the main controller `main.py` to run the different project phases.

### App Store Analysis

This command will run the full pipeline for app store data (ingest, unify, generate insights) and then automatically launch the Streamlit web app.

```bash
python main.py --phase app-analysis
```

### D2C Campaign Analysis (Phase 5)

This command will run the D2C data analysis pipeline (calculate metrics, generate strategic and creative insights) and then launch the Streamlit web app.

```bash
python main.py --phase d2c
```

## Deliverables Checklist

- [x] **1. Clean combined dataset**: `outputs/combined_apps.csv` is generated.
- [x] **2. Insights JSON file**: `outputs/insights.json` is generated with confidence scores.
- [x] **3. Executive report**: `outputs/executive_report.md` is generated.
- [x] **4. CLI/Streamlit interface**: Both `src/cli.py` and `streamlit_app.py` are implemented.
- [x] **5. Phase 5 Extension**: `run_phase5.py` generates funnel insights and creative outputs, viewable in the Streamlit app.