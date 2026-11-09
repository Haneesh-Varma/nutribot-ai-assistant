import os
import unittest
from unittest.mock import Mock, patch

import app as nutribot_app


class NutriBotTests(unittest.TestCase):
    def setUp(self):
        self.client = nutribot_app.app.test_client()

    def test_empty_message_is_rejected(self):
        response = self.client.post("/chat", json={"message": "   "})
        self.assertEqual(response.status_code, 400)

    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    @patch("app.requests.post")
    def test_chat_returns_ai_reply(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Lentils are one useful option."}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        response = self.client.post("/chat", json={"message": "Protein sources?"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["reply"], "Lentils are one useful option.")

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key_returns_service_error(self):
        response = self.client.post("/chat", json={"message": "Hello"})
        self.assertEqual(response.status_code, 503)


if __name__ == "__main__":
    unittest.main()
