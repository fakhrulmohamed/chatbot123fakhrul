"""
Unit tests for Crescent Institute of Science & Technology FAQ Chatbot.
"""

import unittest
import json
from app import app

class TestCrescentFAQChatbot(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Crescent", response.data)

    def test_categories_api(self):
        response = self.client.get("/api/categories")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("categories", data)
        self.assertIn("Admissions & CIEAT", data["categories"])
        self.assertIn("Fees & Scholarships", data["categories"])

    def test_cieat_query(self):
        response = self.client.post(
            "/api/chat",
            data=json.dumps({"message": "tell me about cieat entrance exam"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get("matched"))
        self.assertIn("cieat", data.get("answer").lower())

    def test_btech_fee_query(self):
        response = self.client.post(
            "/api/chat",
            data=json.dumps({"message": "what is the fee structure for btech cse"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get("matched"))
        self.assertIn("fee", data.get("answer").lower())

    def test_kba_hostel_query(self):
        response = self.client.post(
            "/api/chat",
            data=json.dumps({"message": "hostel facilities and kba room charges"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get("matched"))
        self.assertTrue("hostel" in data.get("answer").lower() or "kba" in data.get("answer").lower())

    def test_crescent_contact_query(self):
        response = self.client.post(
            "/api/chat",
            data=json.dumps({"message": "how to contact crescent admissions office"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get("matched"))
        self.assertIn("95432", data.get("answer"))

    def test_greeting_vanakkam(self):
        response = self.client.post(
            "/api/chat",
            data=json.dumps({"message": "vanakkam"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get("type"), "greeting")

if __name__ == "__main__":
    unittest.main()
