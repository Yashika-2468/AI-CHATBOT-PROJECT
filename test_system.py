"""
Automated Verification & Test Suite for CampusIQ AI University Chatbot
Tests AI Engine, Database, and API response contracts.
"""

import unittest
from ai_engine import ai_engine
import database


class TestUniversityChatbot(unittest.TestCase):

    def setUp(self):
        self.engine = ai_engine

    def test_course_inquiry(self):
        res = self.engine.get_response("What engineering courses do you offer?")
        self.assertEqual(res["intent"], "course")
        self.assertGreater(res["confidence"], 0.50)
        self.assertIn("reply", res)
        self.assertFalse(res["is_fallback"])

    def test_fee_inquiry(self):
        res = self.engine.get_response("How much are the college fees?")
        self.assertEqual(res["intent"], "fees")
        self.assertGreater(res["confidence"], 0.50)
        self.assertIn("Fee Breakdown", res["reply"])

    def test_mess_timetable_inquiry(self):
        res = self.engine.get_response("Can you share the hostel mess timetable and menu?")
        self.assertEqual(res["intent"], "Mess Timetable")
        self.assertGreater(res["confidence"], 0.50)
        self.assertIn("Weekly Mess Schedule", res["reply"])

    def test_hod_inquiry(self):
        res = self.engine.get_response("Who is the computer engineering hod?")
        self.assertEqual(res["intent"], "computerhod")
        self.assertGreater(res["confidence"], 0.50)

    def test_database_logging_and_analytics(self):
        # Log a test feedback
        ok = database.log_feedback("test_session", "test query", "course", 1, "great answer")
        self.assertTrue(ok)

        # Retrieve summary
        summary = database.get_analytics_summary()
        self.assertIn("total_queries", summary)
        self.assertIn("avg_confidence", summary)
        self.assertIn("top_intents", summary)

    def test_intents_catalog(self):
        catalog = self.engine.get_all_intents_catalog()
        self.assertEqual(len(catalog), 39)
        for item in catalog:
            self.assertIn("intent", item)
            self.assertIn("category", item)
            self.assertIn("examples", item)


if __name__ == "__main__":
    unittest.main()
