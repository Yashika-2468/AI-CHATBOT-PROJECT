"""
Production Deep Neural Network Model Trainer
Trains an MLP (Multi-Layer Perceptron) Neural Network Intent Classifier
using Scikit-Learn TF-IDF + Neural Pipeline on data/intents.json.
Exports artifacts to model/intent_neural_pipeline.joblib and model/model_meta.json.
"""

import os
import json
import re
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "intents.json")
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "intent_neural_pipeline.joblib")
META_PATH = os.path.join(MODEL_DIR, "model_meta.json")

os.makedirs(MODEL_DIR, exist_ok=True)


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    return " ".join(text.split())


def train_model():
    print("==================================================")
    print("   UNIVERSITY AI CHATBOT — NEURAL MODEL TRAINING   ")
    print("==================================================")
    print(f"\n[1/4] Loading training dataset from {DATA_FILE}...")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    intents = data.get("intents", [])
    texts = []
    labels = []

    for item in intents:
        tag = item["intent"]
        for q in item.get("text", []):
            cleaned = clean_text(q)
            if cleaned:
                texts.append(cleaned)
                labels.append(tag)

    print(f"Total training examples: {len(texts)}")
    print(f"Total intent classes: {len(set(labels))}")

    # Build High-Performance Neural Pipeline
    # TfidfVectorizer with word 1-3 ngrams & sublinear tf
    # Followed by a 2-hidden layer Multi-Layer Perceptron (MLP) Neural Network
    print("\n[2/4] Constructing TF-IDF + Deep MLP Neural Network Pipeline...")
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 3),
            sublinear_tf=True,
            max_features=1500,
            token_pattern=r"(?u)\b\w+\b"
        )),
        ("mlp", MLPClassifier(
            hidden_layer_sizes=(128, 64),
            activation="relu",
            solver="adam",
            alpha=0.0001,
            batch_size=16,
            learning_rate_init=0.003,
            max_iter=350,
            random_state=42,
            early_stopping=False
        ))
    ])

    print("\n[3/4] Fitting Neural Network on university intent patterns...")
    pipeline.fit(texts, labels)

    train_preds = pipeline.predict(texts)
    accuracy = accuracy_score(labels, train_preds)
    print(f"Training Complete! Neural Network Accuracy: {accuracy * 100:.2f}%")

    # Export Model & Metadata
    print("\n[4/4] Exporting model artifacts to model/ directory...")
    joblib.dump(pipeline, MODEL_PATH)

    meta = {
        "model_type": "TF-IDF + Multi-Layer Perceptron Neural Network (MLP)",
        "accuracy": round(float(accuracy), 4),
        "total_samples": len(texts),
        "total_classes": len(pipeline.classes_),
        "classes": list(pipeline.classes_),
        "architecture": "Input (TF-IDF N-Grams) -> Dense(128, ReLU) -> Dense(64, ReLU) -> Softmax(39)"
    }

    with open(META_PATH, "w", encoding="utf-8") as mf:
        json.dump(meta, mf, indent=2)

    print(f"Model saved to: {MODEL_PATH}")
    print(f"Metadata saved to: {META_PATH}")
    print("\nModel Training successfully finished!")


if __name__ == "__main__":
    train_model()
