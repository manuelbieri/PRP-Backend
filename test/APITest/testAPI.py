from fastapi.testclient import TestClient

import API.API as API
import unittest


class APITest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(API.app)

    def test_setup(self):
        response = self.client.get("/items")
        self.assertEqual(200, response.status_code)
        self.assertEqual([{'description': 'this is a test item.', 'id': 1, 'title': 'test item'},
                          {'description': 'this is a second test item.', 'id': 2, 'title': 'second test'}],
                         response.json())
