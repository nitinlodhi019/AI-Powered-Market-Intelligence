# src/report_gen.py

import json
import os


def generate_markdown_report(insights_data):
    """Generates a markdown report from the insights data."""
    report_lines = ["# AI-Powered Market Intelligence Report\n\n"]
    report_lines.append("This report contains automatically generated insights for top Google Play Store apps.\n\n")

    for insight in insights_data:
        app_name = insight.get("app_name", "N/A")
        generated_insight = insight.get("insight", "No insight generated.")

        report_lines.append(f"## Insight for: {app_name}\n")
        report_lines.append(f"**Generated Insight:**\n")
        # Adding a blockquote for better formatting
        report_lines.append(f"> {generated_insight.replace(chr(10), ' ')}\n\n")

    return "".join(report_lines)


if __name__ == '__main__':
    INSIGHTS_JSON_PATH = "outputs/insights.json"
    REPORT_MD_PATH = "outputs/executive_report.md"

    print(f"Reading insights from {INSIGHTS_JSON_PATH}...")
    try:
        with open(INSIGHTS_JSON_PATH, 'r', encoding='utf-8') as f:
            insights = json.load(f)

        print("Generating markdown report...")
        report_content = generate_markdown_report(insights)

        with open(REPORT_MD_PATH, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"Successfully saved executive report to {REPORT_MD_PATH}")

    except FileNotFoundError:
        print(f"Error: Could not find {INSIGHTS_JSON_PATH}. Please run the main pipeline first.")
    except Exception as e:
        print(f"An error occurred: {e}")