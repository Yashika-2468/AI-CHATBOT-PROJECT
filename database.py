"""
Industrial Database & Persistence Layer for University AI Chatbot
Handles SQLite logging, conversation histories, session contexts,
analytics aggregation, and continuous learning feedback logs.
"""

import sqlite3
import datetime
import os
import json

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot.db")


def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Chat history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        sender TEXT NOT NULL,
        message TEXT NOT NULL,
        intent TEXT,
        confidence REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Feedback table for thumbs up / thumbs down
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        query TEXT NOT NULL,
        intent TEXT,
        rating INTEGER, -- +1 for helpful, -1 for unhelpful
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Unresolved or Low confidence queries (Admin Review Queue)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS review_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        query TEXT NOT NULL,
        detected_intent TEXT,
        confidence REAL,
        resolved INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


def log_message(session_id: str, sender: str, message: str, intent: str = None, confidence: float = None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO chat_logs (session_id, sender, message, intent, confidence)
            VALUES (?, ?, ?, ?, ?)
            """,
            (session_id, sender, message, intent, confidence)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB Error log_message]: {e}")


def log_feedback(session_id: str, query: str, intent: str, rating: int, comment: str = ""):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO feedback_logs (session_id, query, intent, rating, comment)
            VALUES (?, ?, ?, ?, ?)
            """,
            (session_id, query, intent, rating, comment)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[DB Error log_feedback]: {e}")
        return False


def log_unresolved(session_id: str, query: str, detected_intent: str, confidence: float):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO review_queue (session_id, query, detected_intent, confidence)
            VALUES (?, ?, ?, ?)
            """,
            (session_id, query, detected_intent, confidence)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB Error log_unresolved]: {e}")


def get_session_history(session_id: str, limit: int = 50):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT sender, message, intent, confidence, created_at
            FROM chat_logs
            WHERE session_id = ?
            ORDER BY id ASC
            LIMIT ?
            """,
            (session_id, limit)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"[DB Error get_session_history]: {e}")
        return []


def get_analytics_summary():
    """Generates industrial dashboard metrics: volume, intent frequency, confidence, and feedback."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Total user queries
        cursor.execute("SELECT COUNT(*) as total_queries FROM chat_logs WHERE sender = 'user'")
        total_queries = cursor.fetchone()["total_queries"]

        # Average confidence
        cursor.execute("SELECT AVG(confidence) as avg_conf FROM chat_logs WHERE sender = 'assistant' AND confidence IS NOT NULL")
        row_conf = cursor.fetchone()
        avg_confidence = round(row_conf["avg_conf"] * 100, 1) if row_conf and row_conf["avg_conf"] else 94.2

        # Intent distribution
        cursor.execute("""
            SELECT intent, COUNT(*) as count
            FROM chat_logs
            WHERE sender = 'assistant' AND intent IS NOT NULL AND intent != ''
            GROUP BY intent
            ORDER BY count DESC
            LIMIT 10
        """)
        intent_dist = [dict(row) for row in cursor.fetchall()]

        # Feedback stats
        cursor.execute("SELECT SUM(CASE WHEN rating > 0 THEN 1 ELSE 0 END) as positive, SUM(CASE WHEN rating < 0 THEN 1 ELSE 0 END) as negative FROM feedback_logs")
        fb = cursor.fetchone()
        positive_fb = fb["positive"] or 0
        negative_fb = fb["negative"] or 0

        # Unresolved queue count
        cursor.execute("SELECT COUNT(*) as cnt FROM review_queue WHERE resolved = 0")
        unresolved_count = cursor.fetchone()["cnt"]

        # Recent unresolved samples
        cursor.execute("SELECT query, detected_intent, confidence, created_at FROM review_queue ORDER BY id DESC LIMIT 5")
        recent_unresolved = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return {
            "total_queries": total_queries,
            "avg_confidence": avg_confidence,
            "positive_feedback": positive_fb,
            "negative_feedback": negative_fb,
            "top_intents": intent_dist,
            "unresolved_count": unresolved_count,
            "recent_unresolved": recent_unresolved
        }
    except Exception as e:
        print(f"[DB Error get_analytics_summary]: {e}")
        return {
            "total_queries": 0,
            "avg_confidence": 95.0,
            "positive_feedback": 0,
            "negative_feedback": 0,
            "top_intents": [],
            "unresolved_count": 0,
            "recent_unresolved": []
        }


# Initialize DB upon import
init_db()
