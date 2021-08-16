import os.path
import flask.testing

import APITest.testAPI as testAPI
import database.ToDoDatabase as dB
import testUtilities.databaseTestUtilities as dataUt

import API.APIUtilities
import API.ToDoAPI
import API.FullAPI


class ToDoAPITest(testAPI.APITest):
    testAPI.APITest.path = os.path.join(os.path.dirname(__file__), testAPI.APITest.database_name)

    def setUpAPIClient(self) -> flask.testing.FlaskClient:
        test_client: flask.testing.FlaskClient = API.FullAPI.app.test_client()
        response = test_client.post(ToDoAPITest.api_base_path + '/login?username=admin&password=adminTest')
        self.headers = {'Authorization': 'Bearer {}'.format(response.json)}
        return test_client

    def setUpDatabase(self) -> None:
        API.ToDoAPI.data = dB.ToDoDatabase(testAPI.APITest.database_name, 'items', os.path.dirname(testAPI.APITest.path))
        dataUt.addDataToTable(API.ToDoAPI.data, dataUt.todoValues)

    def tearDown(self) -> None:
        API.ToDoAPI.data.cleanUpDatabase()

    @classmethod
    def tearDownClass(cls) -> None:
        API.ToDoAPI.data.closeDatabase()
        testAPI.APITest.tearDownClass()

    def test_get_all_todos(self):
        response = self.app.get(ToDoAPITest.api_base_path + '/todo/index', headers=self.headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(4, len(response.json))

    def test_get_selected_todos_multiple_results(self):
        response = self.app.get(ToDoAPITest.api_base_path + '/todo?key=title&value=light', headers=self.headers)
        self.assertEqual(2, len(response.json))

    def test_get_selected_todos_single_result(self):
        response = self.app.get(ToDoAPITest.api_base_path + '/todo?key=title&value=Shopping', headers=self.headers)
        self.assertEqual(1, len(response.json))

    def test_get_selected_todos_invalid_key(self):
        response = self.app.get(ToDoAPITest.api_base_path + '/todo?key=invalid&value=Shopping', headers=self.headers)
        self.assertEqual('Database Error', response.json['message'])

    def test_add_new_valid_todo(self):
        response = self.app.post(ToDoAPITest.api_base_path + '/todo?title=test todo&description=This is a description.', headers=self.headers)
        self.assertEqual('success', response.json['type'])
        response = self.app.get(ToDoAPITest.api_base_path + '/todo/index', headers=self.headers)
        self.assertEqual(5, len(response.json))

    def test_add_new_invalid_todo(self):
        response = self.app.post(ToDoAPITest.api_base_path + '/todo?description=This is a description.', headers=self.headers)
        self.assertEqual('exception', response.json['type'])
        response = self.app.get(ToDoAPITest.api_base_path + '/todo/index', headers=self.headers)
        self.assertEqual(4, len(response.json))

    def test_delete_todo_valid_id(self):
        response = self.app.delete(ToDoAPITest.api_base_path + '/todo?id=1', headers=self.headers)
        self.assertEqual('success', response.json['type'])
        response = self.app.get(ToDoAPITest.api_base_path + '/todo/index', headers=self.headers)
        self.assertEqual(3, len(response.json))

    def test_delete_todo_invalid_id(self):
        response = self.app.delete(ToDoAPITest.api_base_path + '/todo?id=0', headers=self.headers)
        self.assertEqual('exception', response.json['type'])
        response = self.app.get(ToDoAPITest.api_base_path + '/todo/index', headers=self.headers)
        self.assertEqual(4, len(response.json))

    def test_update_valid_args(self):
        response = self.app.put(ToDoAPITest.api_base_path + '/todo?id=1&title=New Title&description=New Des.', headers=self.headers)
        self.assertEqual('success', response.json['type'])
        response = self.app.get(ToDoAPITest.api_base_path + '/todo?key=id&value=1', headers=self.headers)
        self.assertEqual(1, len(response.json))
        self.assertEqual('New Title', response.json[0]['title'])

    def test_update_invalid_args(self):
        response = self.app.put(ToDoAPITest.api_base_path + '/todo?id=0&title=New Title&description=New Des.', headers=self.headers)
        self.assertEqual('exception', response.json['type'])
        response = self.app.get(ToDoAPITest.api_base_path + '/todo?key=id&value=1', headers=self.headers)
        self.assertEqual(1, len(response.json))
        self.assertEqual('Shopping', response.json[0]['title'])

    def test_update_invalid_none_args(self):
        response = self.app.put(ToDoAPITest.api_base_path + '/todo?id=0&description=New Des.', headers=self.headers)
        self.assertEqual('exception', response.json['type'])

    def test_valid_login(self):
        response = self.app.post(ToDoAPITest.api_base_path + '/login?username=admin&password=adminTest')
        self.assertEqual(200, response.status_code)
        response = self.app.get(ToDoAPITest.api_base_path + '/user', headers={'Authorization': 'Bearer {}'.format(response.json)})
        self.assertEqual(1, response.json)
