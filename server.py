"""
Industrial FastAPI Backend Server for CampusIQ AI University Portal
Provides REST APIs for real-time chat, analytics, knowledge directory,
model diagnostics sandbox, and static web page hosting.
"""

import os
import uvicorn
from typing import Optional, List
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import database
from ai_engine import ai_engine, TAG_TO_CATEGORY

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
ANALYTICS_DIR = os.path.join(BASE_DIR, "analytics_output")

app = FastAPI(
    title="AI-Powered Chatbot for University Student Support — Yashika Gupta (ABES)",
    description="HCLTech Career Shaper Programme 2026–27 | Mentor: Dr. Anamika Goel | ABES Engineering College",
    version="1.0.0"
)

# CORS Middleware for university cross-origin integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
if os.path.exists(ANALYTICS_DIR):
    app.mount("/analytics_output", StaticFiles(directory=ANALYTICS_DIR), name="analytics_output")


# Pydantic Schemas
class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = "guest_session"


class FeedbackRequest(BaseModel):
    session_id: str
    query: str
    intent: str
    rating: int  # +1 or -1
    comment: Optional[str] = ""


class SandboxRequest(BaseModel):
    query: str


# Root Endpoint - Serves Modern Portal
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = os.path.join(TEMPLATES_DIR, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h2>CampusIQ portal loading...</h2>")


@app.get("/download-zip")
async def download_zip():
    """Direct one-click download for the project ZIP file."""
    zip_path = os.path.join(BASE_DIR, "AI_University_Chatbot_HCL_Submission.zip")
    if os.path.exists(zip_path):
        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename="AI_University_Chatbot_HCL_Submission.zip"
        )
    return {"error": "ZIP file not found"}


# 1. Main Chat Endpoint
@app.post("/api/chat")
async def chat_endpoint(payload: ChatRequest):
    """Processes user query and returns classified intent, rich answer, and suggestions."""
    response = ai_engine.get_response(payload.query, payload.session_id)
    return response


# 2. User Feedback Endpoint
@app.post("/api/feedback")
async def feedback_endpoint(payload: FeedbackRequest):
    """Logs user satisfaction ratings (+1 or -1) to the SQLite audit database."""
    success = database.log_feedback(
        session_id=payload.session_id,
        query=payload.query,
        intent=payload.intent,
        rating=payload.rating,
        comment=payload.comment or ""
    )
    return {"status": "success" if success else "failed"}


# 3. Analytics Endpoint
@app.get("/api/analytics")
async def analytics_endpoint():
    """Returns aggregated executive analytics and unhandled query queues."""
    summary = database.get_analytics_summary()
    return summary


# 4. Knowledge Base Catalog Endpoint
@app.get("/api/intents")
async def intents_catalog_endpoint():
    """Returns all 39 indexed university intents grouped by category."""
    catalog = ai_engine.get_all_intents_catalog()
    return catalog


# 5. Session History Endpoint
@app.get("/api/history/{session_id}")
async def session_history_endpoint(session_id: str):
    """Returns conversation history for a given session."""
    history = database.get_session_history(session_id)
    return {"session_id": session_id, "messages": history}


# 6. Model Diagnostic Sandbox Endpoint
@app.post("/api/sandbox")
async def sandbox_endpoint(payload: SandboxRequest):
    """Detailed model diagnostic breakdown showing probability distributions across classes."""
    top_intent, confidence, matched_sample, ranked = ai_engine.predict_intent(payload.query)
    category = TAG_TO_CATEGORY.get(top_intent, "General")

    ranked_list = []
    if ranked:
        for tag, score in ranked[:8]:
            ranked_list.append({"intent": tag, "score": round(score, 4)})

    return {
        "query": payload.query,
        "top_intent": top_intent,
        "confidence": confidence,
        "category": category,
        "matched_sample": matched_sample,
        "ranked_predictions": ranked_list
    }


# 7. Health & Diagnostics
@app.get("/api/health")
async def health_check():
    """Verifies backend server health and model operational state."""
    has_neural = ai_engine.neural_pipeline is not None
    return {
        "status": "healthy",
        "service": "CampusIQ Enterprise University AI",
        "neural_model_loaded": has_neural,
        "total_intents": len(ai_engine.intents),
        "database": "SQLite (Active)"
    }


def open_browser():
    """Automatically launches Firefox as soon as server starts."""
    import time
    time.sleep(1.0)
    firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    url = "http://127.0.0.1:8000"
    if os.path.exists(firefox_path):
        os.system(f'start "" "{firefox_path}" "{url}"')
    else:
        import webbrowser
        webbrowser.open(url)


if __name__ == "__main__":
    import threading
    print("==================================================")
    print("  STARTING UNIVERSITY AI HELPDESK SERVER          ")
    print("  Portal URL: http://127.0.0.1:8000                ")
    print("  Opening automatically in Mozilla Firefox...      ")
    print("==================================================")
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
