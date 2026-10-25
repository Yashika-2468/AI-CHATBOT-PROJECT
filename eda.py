"""
Industrial Exploratory Data Analysis (EDA) Pipeline
Analyzes data/intents.json:
- Computes intent distributions, vocabulary sizes, and character lengths
- Generates and exports publication-ready statistical visualizations to analytics_output/
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "intents.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "analytics_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_eda():
    print("==================================================")
    print("   UNIVERSITY DATASET EXPLORATORY DATA ANALYSIS   ")
    print("==================================================")

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    intents = data["intents"]
    print(f"\n1. Total Unique Institutional Intents: {len(intents)}")

    rows = []
    for item in intents:
        tag = item["intent"]
        for q in item.get("text", []):
            rows.append({
                "intent": tag,
                "question": q,
                "length_chars": len(q),
                "word_count": len(q.split())
            })

    df = pd.DataFrame(rows)
    print(f"2. Total Pattern Questions Indexed: {len(df)}")
    print(f"3. Average Question Word Count: {df['word_count'].mean():.2f} words")
    print(f"4. Missing Values Detected: {df.isnull().sum().to_dict()}")

    print("\nTop 10 Most Inquired Intents by Training Volume:")
    print(df["intent"].value_counts().head(10))

    # Graph 1: Intent Distribution
    plt.figure(figsize=(14, 7))
    intent_counts = df["intent"].value_counts()
    bars = plt.bar(intent_counts.index, intent_counts.values, color="#4f46e5", edgecolor="#312e81")
    plt.title("Distribution of Training Questions Across University Intents", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Intent Tag", fontsize=11, labelpad=10)
    plt.ylabel("Sample Question Count", fontsize=11, labelpad=10)
    plt.xticks(rotation=90, fontsize=8)
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    chart1_path = os.path.join(OUTPUT_DIR, "eda_intent_distribution.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"\n[Saved Chart 1]: {chart1_path}")

    # Graph 2: Question Length Distribution
    plt.figure(figsize=(9, 5))
    plt.hist(df["word_count"], bins=15, color="#10b981", edgecolor="#047857", alpha=0.85)
    plt.title("Student Question Length Distribution (Word Count)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Number of Words per Query", fontsize=10)
    plt.ylabel("Frequency", fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    chart2_path = os.path.join(OUTPUT_DIR, "eda_word_length_distribution.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"[Saved Chart 2]: {chart2_path}")

    print("\nEDA Pipeline Completed Successfully!")


if __name__ == "__main__":
    run_eda()
