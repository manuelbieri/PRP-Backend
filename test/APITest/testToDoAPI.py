import os.path
import APITest.testAPI as testAPI
import database.ToDoDatabase as dB
from testUtilities.databaseUtilities import *

import API.ToDoAPI


class ToDoAPITest(testAPI.APITest):
    testAPI.APITest.base_path = '/api/v1/todo'
    testAPI.APITest.path = os.path.join(os.path.dirname(__file__), testAPI.APITest.database_name)

    def setUpAPIClient(self):
        return API.ToDoAPI.app.test_client()

    def setUpDatabase(self) -> None:
        API.ToDoAPI.data = dB.ToDoDatabase(testAPI.APITest.database_name, 'items', os.path.dirname(testAPI.APITest.path))

    @classmethod
    def tearDownClass(cls) -> None:
        API.ToDoAPI.data.closeDatabase()
        testAPI.APITest.tearDownClass()

    def test_get_all_items(self):
        response = self.app.get(ToDoAPITest.base_path + '/items/index')
        self.assertEqual(200, response.status_code)
        self.assertEqual(4, len(response.json))

    def test_get_single_items_multiple_possible_results(self):
        response = self.app.get(ToDoAPITest.base_path + '/item?key=title&value=light')
        self.assertEqual('Lights for the dining room', response.json['description'])

    def test_get_single_items_single_possible_result(self):
        response = self.app.get(ToDoAPITest.base_path + '/item?key=id&value=1')
        self.assertEqual('Shopping', response.json['title'])

    def test_get_selected_items_multiple_results(self):
        response = self.app.get(ToDoAPITest.base_path + '/items?key=title&value=light')
        self.assertEqual(2, len(response.json))

    def test_get_selected_items_single_result(self):
        response = self.app.get(ToDoAPITest.base_path + '/items?key=title&value=Shopping')
        self.assertEqual(1, len(response.json))

    def test_get_selected_items_invalid_key(self):
        response = self.app.get(ToDoAPITest.base_path + '/items?key=invalid&value=Shopping')
        self.assertEqual('Database Error', response.json['message'])

    def test_get_single_items_invalid_key(self):
        response = self.app.get(ToDoAPITest.base_path + '/item?key=invalid&value=Shopping')
        self.assertEqual('Database Error', response.json['message'])

    def test_add_new_valid_item(self):
        response = self.app.post(ToDoAPITest.base_path + '/item?title=test item&description=This is a description.')
        self.assertEqual('success', response.json['type'])
        response = self.app.get(ToDoAPITest.base_path + '/items/index')
        self.assertEqual(5, len(response.json))

    def test_add_new_invalid_item(self):
        response = self.app.post(ToDoAPITest.base_path + '/item?description=This is a description.')
        self.assertEqual('exception', response.json['type'])
        response = self.app.get(ToDoAPITest.base_path + '/items/index')
        self.assertEqual(4, len(response.json))

    def test_delete_item_valid_id(self):
        response = self.app.delete(ToDoAPITest.base_path + '/item?id=1')
        self.assertEqual('success', response.json['type'])
        response = self.app.get(ToDoAPITest.base_path + '/items/index')
        self.assertEqual(3, len(response.json))

    def test_delete_item_invalid_id(self):
        response = self.app.delete(ToDoAPITest.base_path + '/item?id=0')
        self.assertEqual('exception', response.json['type'])
        response = self.app.get(ToDoAPITest.base_path + '/items/index')
        self.assertEqual(4, len(response.json))

    def test_update_valid_args(self):
        response = self.app.put(ToDoAPITest.base_path + '/item?id=1&title=New Title&description=New Des.')
        self.assertEqual('success', response.json['type'])
        response = self.app.get(ToDoAPITest.base_path + '/item?key=id&value=1')
        self.assertEqual('New Title', response.json['title'])

    def test_update_invalid_args(self):
        response = self.app.put(ToDoAPITest.base_path + '/item?id=0&title=New Title&description=New Des.')
        self.assertEqual('exception', response.json['type'])
        response = self.app.get(ToDoAPITest.base_path + '/item?key=id&value=1')
        self.assertEqual('Shopping', response.json['title'])

    def test_update_invalid_none_args(self):
        response = self.app.put(ToDoAPITest.base_path + '/item?id=0&description=New Des.')
        self.assertEqual('exception', response.json['type'])
