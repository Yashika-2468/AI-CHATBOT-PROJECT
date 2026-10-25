# 🎓 CampusIQ — Industrial AI University Intelligence & Chatbot Portal

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20REST%20API-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit%20Enterprise-FF4B4B.svg)](https://streamlit.io)
[![Model Accuracy](https://img.shields.io/badge/Neural%20Accuracy-99.51%25-brightgreen.svg)](#ai--nlp-architecture)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](#)

**CampusIQ** is an end-to-end, industrial-grade AI-powered Student Support Portal designed for higher education institutions, engineering colleges, and universities. Built upon 39 distinct institutional knowledge intents (admissions, fee schedules, hostel amenities, weekly mess timetable, placement records, syllabi, faculty directories, and campus security), the system provides sub-millisecond, highly calibrated responses via both a **Modern Glassmorphic Web Portal** and an **Enterprise Streamlit Dashboard**.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    User([🧑‍🎓 Student / Parent / Applicant]) --> |Voice / Text Input| UI[CampusIQ Modern Web Portal / Streamlit Dashboard]
    
    subgraph Frontend [Presentation Layer]
        UI --> Tab1[💬 Conversational AI Hub]
        UI --> Tab2[📚 Knowledge Directory (39 Intents)]
        UI --> Tab3[🎓 Admission & Fee Estimator]
        UI --> Tab4[📊 Executive Analytics Dashboard]
        UI --> Tab5[🧪 Model Diagnostic Sandbox]
    end

    subgraph API [FastAPI REST Gateway :8000]
        Tab1 --> |POST /api/chat| ChatEp[/api/chat]
        Tab1 --> |POST /api/feedback| FbEp[/api/feedback]
        Tab2 --> |GET /api/intents| IntentEp[/api/intents]
        Tab4 --> |GET /api/analytics| AnalyticsEp[/api/analytics]
        Tab5 --> |POST /api/sandbox| SandboxEp[/api/sandbox]
    end

    subgraph AIEngine [Hybrid Ensemble AI Engine]
        ChatEp --> NlpPre[Text Normalization & Entity Disambiguation]
        NlpPre --> Ensemble[Ensemble Classifier]
        
        Ensemble --> Neural[Deep MLP Neural Network - 99.5%]
        Ensemble --> WordTfidf[Word N-Gram TF-IDF Vectorizer]
        Ensemble --> CharTfidf[Character N-Gram Typo-Tolerant Matcher]
        
        Neural & WordTfidf & CharTfidf --> Calibrator[Confidence Calibration & Multi-Turn Context]
        Calibrator --> RichFmt[Rich Response Formatter & Suggestion Generator]
    end

    subgraph Persistence [SQLite Storage Layer]
        RichFmt --> |Audit Logs| DB[(chatbot.db)]
        FbEp --> |Thumbs Up/Down| DB
        Calibrator --> |Fallback Queue| DB
        DB --> |Aggregated KPIs| AnalyticsEp
    end
```

---

## 🚀 Key Industrial Features

### 1. 💬 Next-Gen AI Assistant
- **Dual-Layer Hybrid NLP**: Combines a Deep Multi-Layer Perceptron (MLP) Neural Network with sublinear word & character-level TF-IDF n-grams to guarantee typo tolerance, phrase variations, and contextual accuracy.
- **Voice-Enabled Interface**: Integrated **Web Speech Recognition** (Speech-to-Text) and **Web Speech Synthesis** (Voice Narration) for full accessibility.
- **Contextual State Machine**: Tracks multi-turn conversational context (e.g., following up on admissions with *"how much does it cost?"* maintains the context).
- **Rich Markdown Formatting**: Auto-generates structured tables, weekly hostel mess timetables, fee breakdowns, and HOD contact cards.
- **Related Suggestion Chips**: Dynamically surfaces relevant follow-up topics to guide user navigation.

### 2. 📚 Institutional Knowledge Directory
- Visual browser indexing all 39 university intents categorized across:
  - **Admissions & Fees**
  - **Academics & Faculty**
  - **Campus & Facilities**
  - **Student Affairs & Placements**
  - **General & Administrative**
- Real-time keyword search and one-click *"Ask Chatbot"* routing.

### 3. 🎓 Student Admission & Fee Estimator
- Interactive calculator for annual tuition, lab charges, on-campus AC/Non-AC hostel, mess meal plans, bus commute, and laptop bundles.
- Automatically calculates category waivers (OBC, SC/ST, TFWS) and merit scholarships based on entrance percentiles.

### 4. 📊 Executive Analytics & Review Queue
- Live telemetry from `chatbot.db`: Total inquiries, average neural confidence rate, student satisfaction percentage, and trending intent charts.
- **Continuous Learning Queue**: Fallback or low-confidence queries are automatically logged for administrative review and training data enrichment.

### 5. 🧪 Model Diagnostic Sandbox & Open REST API
- Real-time probability inspector across all 39 intent classes.
- Built-in interactive **Swagger UI Documentation** at `http://127.0.0.1:8000/docs`.

---

## 📂 Project Structure

```
AI university chatbot/
│
├── data/
│   └── intents.json                 # Core dataset (39 university intents, 412 patterns)
│
├── model/
│   ├── intent_neural_pipeline.joblib# Trained Deep MLP Neural Pipeline (99.5% accuracy)
│   └── model_meta.json              # Model parameters, classes, and metadata
│
├── analytics_output/
│   ├── eda_intent_distribution.png  # Statistical distribution chart
│   └── eda_word_length_distribution.png # Query length histogram
│
├── templates/
│   └── index.html                   # Modern responsive Web Portal UI
│
├── static/
│   ├── style.css                    # Industrial design system (Dark/Light glassmorphism)
│   └── app.js                       # Frontend state, speech, and API integrations
│
├── ai_engine.py                     # Unified Ensemble AI & NLP engine
├── database.py                      # SQLite persistence and analytics aggregator
├── train_model.py                   # Deep learning neural network trainer
├── eda.py                           # Dataset statistical analysis & chart generator
├── server.py                        # Industrial FastAPI application
├── app.py                           # Multi-tab Streamlit Enterprise Dashboard
├── test_system.py                   # Automated unit test suite
├── requirements.txt                 # Python dependencies
├── start_website.bat                # One-click launcher for Web Portal (:8000)
├── start_streamlit.bat              # One-click launcher for Streamlit (:8501)
└── README.md                        # Documentation
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10, 3.11, or 3.12 installed.

### 1. Clone / Navigate to Directory
```powershell
cd "c:\Users\HP\Desktop\AI university chatbot"
```

### 2. Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### 3. (Optional) Re-train the AI Neural Classifier
The trained model is already bundled in `model/`. To retrain from scratch:
```powershell
python train_model.py
```
*Output: Neural Network Accuracy: 99.51%*

---

## 🖥️ Running the Application

### Option A: Modern Web Portal (FastAPI) — Recommended for Industrial Deployment
Double-click `start_website.bat` or run:
```powershell
python server.py
```
- **Web Portal URL**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive REST API Docs (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Option B: Streamlit Enterprise Dashboard — Ideal for Academic Presentations
Double-click `start_streamlit.bat` or run:
```powershell
streamlit run app.py
```
- **Streamlit URL**: [http://localhost:8501](http://localhost:8501)

---

## 🧪 Verification & Unit Testing

Run the automated test suite to verify intent recognition, database logging, and API schemas:
```powershell
python test_system.py
```
*All 6 unit tests verify intent accuracy, department disambiguation, and database telemetry.*

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Serves the CampusIQ web application |
| `/api/chat` | `POST` | Primary conversational AI inference endpoint |
| `/api/feedback` | `POST` | Logs thumbs up (+1) / thumbs down (-1) ratings |
| `/api/analytics`| `GET` | Returns aggregated metrics, KPI cards, and unhandled queries |
| `/api/intents` | `GET` | Returns directory of 39 indexed university intents |
| `/api/history/{id}` | `GET` | Returns chat history for a session |
| `/api/sandbox` | `POST` | Inspects multi-class prediction probabilities |
| `/api/health` | `GET` | Health check and neural pipeline status |

---

## 🏆 Project Evaluation & Viva Guide

- **Q: Why combine TF-IDF and a Deep MLP Neural Network?**
  *A: A pure neural network can overfit on small datasets with varied phrasing, while pure TF-IDF cosine similarity cannot capture non-linear sentence representations. By ensembling 65% Neural probabilities with 35% Word + Character TF-IDF and entity extraction, the chatbot achieves both high semantic precision and 100% typo tolerance.*

- **Q: How does the system handle unknown or malicious queries?**
  *A: The system implements calibrated confidence scoring. Queries scoring below 0.35 trigger a graceful fallback containing popular campus directories and are automatically logged into `review_queue` in SQLite for human-in-the-loop retraining.*
