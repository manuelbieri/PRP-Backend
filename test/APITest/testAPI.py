from fastapi.testclient import TestClient
import main
import unittest


class APITest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(main.app)

    def test_setup(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"msg": "Hello World"})