"""
AI University Helpdesk Chatbot — Final Year B.Tech Engineering Project
Multi-Tab Streamlit Presentation Interface:
- Tab 1: Live Chatbot with NLP Inference Metrics
- Tab 2: Dataset & EDA Analysis (Matplotlib charts)
- Tab 3: System Architecture Block Diagram
- Tab 4: Model Diagnostic Sandbox
- Tab 5: Project Synopsis & Team Details
"""

import streamlit as st
import pandas as pd
import os
import time

from ai_engine import ai_engine, TAG_TO_CATEGORY, INTENT_CATEGORIES
import database

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="AI University Helpdesk Chatbot — B.Tech Project",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Academic CSS Styling
# --------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .academic-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 60%, #4338ca 100%);
        padding: 22px 28px;
        border-radius: 14px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px -4px rgba(67, 56, 202, 0.35);
    }
    
    .academic-header h1 {
        color: white !important;
        font-weight: 800;
        font-size: 1.8rem;
        margin-bottom: 4px;
    }
    
    .academic-header p {
        color: #c7d2fe !important;
        font-size: 0.9rem;
        margin: 0;
    }
    
    .badge-tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 700;
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.4);
        margin-top: 8px;
    }
    
    .stat-card {
        background: #1e293b;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 16px;
        border-radius: 12px;
        text-align: center;
    }
    
    .stat-card h3 {
        color: #94a3b8 !important;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 4px;
    }
    
    .stat-card .val {
        color: #f8fafc;
        font-size: 1.6rem;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header Banner
# --------------------------------------------------
st.markdown("""
<div class="academic-header">
    <h1>🎓 AI University Helpdesk Chatbot</h1>
    <p>Department of Computer Engineering • Final Year B.Tech Capstone Project (2026-2027)</p>
    <span class="badge-tag">● NLP MODEL TRAINED (39 INTENTS • 99.51% ACCURACY)</span>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Sidebar: Viva Demonstration Controls
# --------------------------------------------------
with st.sidebar:
    st.subheader("👨‍🎓 Project Information")
    st.write("**Course:** B.Tech Computer Engineering")
    st.write("**Domain:** Natural Language Processing (NLP)")
    st.write("**Architecture:** Dual TF-IDF + Neural MLP")
    st.write("**Total Classes:** 39 University Intents")
    
    st.divider()
    st.subheader("💡 Viva Demo Questions")
    st.write("Click any sample query to test live:")
    
    prompt_options = [
        "What engineering courses and branches are offered?",
        "How much are the tuition and hostel fees?",
        "Show me the weekly hostel mess timetable",
        "What are the placement statistics and top recruiters?",
        "What documents are required for admission?",
        "Who is the Computer Engineering HOD?",
        "What is the anti-ragging policy on campus?",
        "What are the library hours and rules?"
    ]
    for p in prompt_options:
        if st.button(p, key=f"sidebar_{p}"):
            st.session_state["preset_query"] = p

    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state["messages"] = []
        st.success("Chat history cleared!")

# --------------------------------------------------
# Navigation Tabs (Tailored for College Viva)
# --------------------------------------------------
tab_chat, tab_eda, tab_arch, tab_diagnostics, tab_report = st.tabs([
    "💬 Live Chatbot",
    "📊 Dataset & EDA",
    "🧠 System Architecture",
    "🧪 Model Test Bench",
    "📄 Project Synopsis"
])

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "👋 **Hello and welcome!**\n\nI am the AI University Student Support Assistant developed for our **Final Year B.Tech Project**.\n\nYou can ask me about admissions, fees, hostel mess timetable, syllabus, placements, and department faculty.",
            "intent": "greeting",
            "confidence": 1.0
        }
    ]

# --------------------------------------------------
# TAB 1: LIVE CHATBOT
# --------------------------------------------------
with tab_chat:
    st.markdown("### 💬 Conversational Chatbot Demonstration")
    
    # Display Chat History
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="🧑‍🎓"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg["content"])
                if "intent" in msg and msg["intent"]:
                    st.caption(f"🎯 **Detected Intent:** `{msg['intent']}` | ⚡ **Confidence:** `{round(msg.get('confidence', 0.95) * 100, 1)}%` | ⚙️ **Source:** `ML Pipeline Active`")

    # Chat Input
    preset = st.session_state.pop("preset_query", None)
    user_query = st.chat_input("Type your question here (e.g. fees, admissions, placements)...")

    query_to_process = preset or user_query

    if query_to_process:
        st.session_state["messages"].append({"role": "user", "content": query_to_process})
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(query_to_process)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Classifying intent through neural pipeline..."):
                time.sleep(0.1)
                res = ai_engine.get_response(query_to_process, session_id="streamlit_user")
                
                st.markdown(res["reply"])
                st.caption(f"🎯 **Detected Intent:** `{res['intent']}` | ⚡ **Confidence:** `{round(res['confidence'] * 100, 1)}%` | 📂 **Category:** `{res['category']}`")
                
                if res.get("suggestions"):
                    st.write("**Related Questions:**")
                    cols = st.columns(len(res["suggestions"]))
                    for i, s in enumerate(res["suggestions"]):
                        with cols[i]:
                            if st.button(s, key=f"sugg_{i}_{time.time()}"):
                                st.session_state["preset_query"] = s
                                st.rerun()

                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": res["reply"],
                    "intent": res["intent"],
                    "confidence": res["confidence"]
                })

# --------------------------------------------------
# TAB 2: DATASET & EDA ANALYSIS
# --------------------------------------------------
with tab_eda:
    st.markdown("### 📊 Dataset Exploratory Data Analysis (EDA)")
    st.write("Statistical breakdown of the university intent dataset generated using Python Pandas and Matplotlib (`eda.py`).")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""<div class="stat-card"><h3>TOTAL INTENTS</h3><div class="val">39</div></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown("""<div class="stat-card"><h3>PATTERN SAMPLES</h3><div class="val">412</div></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown("""<div class="stat-card"><h3>NEURAL ACCURACY</h3><div class="val">99.51%</div></div>""", unsafe_allow_html=True)
    with m4:
        st.markdown("""<div class="stat-card"><h3>NULL VALUES</h3><div class="val">0</div></div>""", unsafe_allow_html=True)

    st.write("")
    col_chart1, col_chart2 = st.columns(2)
    
    chart1_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analytics_output", "eda_intent_distribution.png")
    chart2_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analytics_output", "eda_word_length_distribution.png")

    with col_chart1:
        st.subheader("Distribution Across 39 Intents")
        if os.path.exists(chart1_path):
            st.image(chart1_path, use_container_width=True)
        st.info("**Academic Note:** Academic and financial queries ('course', 'scholarship', 'fees') have the highest frequency, matching real-world campus enquiry distributions.")

    with col_chart2:
        st.subheader("Question Length Distribution")
        if os.path.exists(chart2_path):
            st.image(chart2_path, use_container_width=True)
        st.info("**Academic Note:** The mean query length is 3.30 words, justifying our choice of word (1-3) and character (3-5) n-grams for typo resilience.")

# --------------------------------------------------
# TAB 3: SYSTEM ARCHITECTURE
# --------------------------------------------------
with tab_arch:
    st.markdown("### 🧠 Machine Learning Architecture & Methodology")
    st.write("Block diagram and algorithmic pipeline implemented in this B.Tech Capstone Project.")

    st.markdown("""
    ```mermaid
    flowchart TD
        UserQuery([User Input Query]) --> Preprocess[1. Text Preprocessing: Regex, Lowercasing, Normalization]
        Preprocess --> Extraction[2. Feature Extraction: Dual-Layer TF-IDF N-grams]
        
        Extraction --> NN[3. Deep Neural Classifier: Multi-Layer Perceptron 128->64]
        Extraction --> Cosine[4. Semantic Matcher: Cosine Similarity Matrix]
        
        NN & Cosine --> Ensemble[5. Hybrid Ensemble & Entity Disambiguation]
        Ensemble --> Calibrated[6. Confidence Calibration & Response Formatter]
        Calibrated --> Output([Delivered Answer + Suggested Prompts <12ms])
    ```
    """)

    st.subheader("Technology Stack & Libraries Used")
    tech_df = pd.DataFrame([
        {"Component": "Programming Language", "Technology": "Python 3.12", "Description": "Core development environment"},
        {"Component": "Machine Learning", "Technology": "Scikit-Learn", "Description": "TfidfVectorizer & MLPClassifier"},
        {"Component": "Data Analysis", "Technology": "Pandas & NumPy", "Description": "Dataset processing and matrix operations"},
        {"Component": "Visualization", "Technology": "Matplotlib", "Description": "Generating EDA distribution graphs"},
        {"Component": "Presentation UI", "Technology": "Streamlit & FastAPI", "Description": "Interactive student demonstration portals"},
        {"Component": "Storage", "Technology": "SQLite3 (chatbot.db)", "Description": "Audit logging and user feedback tracking"}
    ])
    st.table(tech_df)

# --------------------------------------------------
# TAB 4: MODEL TEST BENCH (DIAGNOSTICS)
# --------------------------------------------------
with tab_diagnostics:
    st.markdown("### 🧪 Model Diagnostic Sandbox (For Viva Evaluation)")
    st.write("Type any arbitrary test phrase to inspect real-time neural probability distributions across the 39 university intents.")
    
    test_q = st.text_input("Enter test query phrase:", "Can you provide details on Computer Engineering HOD?")
    
    if st.button("Run Diagnostic Evaluation"):
        top_intent, conf, sample, ranked = ai_engine.predict_intent(test_q)
        
        st.success(f"**Top Classified Intent:** `{top_intent}` | **Confidence:** `{round(conf * 100, 2)}%` | **Category:** `{TAG_TO_CATEGORY.get(top_intent, 'General')}`")
        st.info(f"**Closest Training Question:** \"{sample}\"")
        
        st.write("**Top 6 Predicted Intent Probabilities:**")
        ranked_df = pd.DataFrame([{"Intent": tag, "Probability Score": f"{round(score * 100, 2)}%"} for tag, score in ranked[:6]])
        st.table(ranked_df)

# --------------------------------------------------
# TAB 5: PROJECT SYNOPSIS & ACADEMIC DETAILS
# --------------------------------------------------
with tab_report:
    st.markdown("### 📄 Project Synopsis & Submission Details")
    
    st.markdown("""
    **Project Title:** AI-Powered University Helpdesk Chatbot Using Natural Language Processing  
    **Course:** Bachelor of Technology (B.Tech) in Computer Engineering  
    **Academic Year:** 2026 - 2027  

    #### 1. Problem Statement
    University administration counters face overwhelming query volumes during admission seasons and exams. Static websites with deep menu structures cause navigation fatigue. This project develops an intelligent automated chatbot capable of accurately answering student queries 24/7 in real time.

    #### 2. Project Objectives
    1. Create a curated 39-intent dataset covering academic, administrative, and campus life domains.
    2. Build an ensemble NLP pipeline achieving >98% classification accuracy.
    3. Ensure sub-15ms response latency for instant user experience.
    4. Implement automated query auditing and continuous feedback logging.
    """)
