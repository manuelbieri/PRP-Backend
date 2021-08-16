import unittest
import flask.testing

import API.FullAPI


class FullAPITest(unittest.TestCase):
    api_base_path = '/api/v1'
    
    def setUp(self) -> None:
        self.app: flask.testing.FlaskClient = API.FullAPI.app.test_client()
        response = self.app.post(FullAPITest.api_base_path + '/login?username=admin&password=adminTest')
        self.headers = {'Authorization': 'Bearer {}'.format(response.json)}

    def test_valid_login(self):
        response = self.app.post(FullAPITest.api_base_path + '/login?username=admin&password=adminTest')
        self.assertEqual(200, response.status_code)
        header = {'Authorization': 'Bearer {}'.format(response.json)}
        response = self.app.get(FullAPITest.api_base_path + '/user', headers=header)
        self.assertEqual(1, response.json)

    def test_invalid_username_login(self):
        response = self.app.post(FullAPITest.api_base_path + '/login?username=invalid&password=adminTest')
        self.assertEqual(200, response.status_code)
        self.assertEqual('Invalid user', response.json.get('message'))

    def test_invalid_password_login(self):
        response = self.app.post(FullAPITest.api_base_path + '/login?username=admin&password=invalid')
        self.assertEqual(200, response.status_code)
        self.assertEqual('Invalid credentials', response.json.get('message'))

    def test_valid_auth_required(self):
        response = self.app.get(FullAPITest.api_base_path + '/user', headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json)

    def test_invalid_auth_required(self):
        response = self.app.get(FullAPITest.api_base_path + '/user')
        self.assertEqual(500, response.status_code)
