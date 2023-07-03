import unittest
import json
from app import app

class TestSQLInjectionDetection(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_sanitized_payload(self):
        payload = {
            "payload": "input"
        }
        response = self.app.post('/v1/sanitized/input/', json=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['result'], 'sanitized')

    def test_unsanitized_payload(self):
        payload = {
            "payload": "input'; DROP TABLE users;"
        }
        response = self.app.post('/v1/sanitized/input/', json=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['result'], 'unsanitized')

    def test_empty_payload(self):
        payload = {}
        response = self.app.post('/v1/sanitized/input/', json=payload)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'No payload provided')

    def test_invalid_payload(self):
        payload = {
            "some_key": "some_value"
        }
        response = self.app.post('/v1/sanitized/input/', json=payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'No payload provided')

if __name__ == '__main__':
    unittest.main()
