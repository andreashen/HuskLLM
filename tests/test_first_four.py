import unittest
from fastapi.testclient import TestClient
from main import app

class TestFirstFourAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_list_models(self):
        r = self.client.get("/v1/models")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data.get("object"), "list")
        self.assertIsInstance(data.get("data"), list)
        self.assertGreaterEqual(len(data["data"]), 1)
        m = data["data"][0]
        self.assertEqual(m.get("object"), "model")
        self.assertIn("id", m)
        self.assertIn("created", m)
        self.assertIn("owned_by", m)

    def test_retrieve_model(self):
        model_id = "gpt-4o-mini"
        r = self.client.get(f"/v1/models/{model_id}")
        self.assertEqual(r.status_code, 200)
        m = r.json()
        self.assertEqual(m.get("object"), "model")
        self.assertEqual(m.get("id"), model_id)
        self.assertIn("created", m)
        self.assertIn("owned_by", m)

    def test_chat_completions(self):
        payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "hi"}]}
        r = self.client.post("/v1/chat/completions", json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data.get("object"), "chat.completion")
        self.assertEqual(data.get("model"), "gpt-4o-mini")
        self.assertIsInstance(data.get("choices"), list)
        self.assertEqual(len(data["choices"]), 1)
        choice = data["choices"][0]
        self.assertEqual(choice.get("finish_reason"), "stop")
        self.assertEqual(choice.get("message", {}).get("role"), "assistant")
        self.assertEqual(choice.get("message", {}).get("content"), "")
        usage = data.get("usage", {})
        self.assertEqual(usage.get("total_tokens"), 0)

    def test_text_completions(self):
        payload = {"model": "gpt-4o-mini", "prompt": "hello"}
        r = self.client.post("/v1/completions", json=payload)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data.get("object"), "text_completion")
        self.assertEqual(data.get("model"), "gpt-4o-mini")
        self.assertIsInstance(data.get("choices"), list)
        self.assertEqual(len(data["choices"]), 1)
        choice = data["choices"][0]
        self.assertEqual(choice.get("finish_reason"), "stop")
        self.assertEqual(choice.get("text"), "")

if __name__ == "__main__":
    unittest.main()

