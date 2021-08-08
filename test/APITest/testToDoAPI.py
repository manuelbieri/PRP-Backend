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

    def test_getAllItems(self):
        response = self.app.get(ToDoAPITest.base_path + '/items/index')
        self.assertEqual(200, response.status_code)
        self.assertEqual(4, len(response.json))

    def test_getSingleItemsMultiplePossibleResults(self):
        response = self.app.get(ToDoAPITest.base_path + '/item?key=title&value=light')
        self.assertEqual('Lights for the dining room', response.json['description'])

    def test_getSingleItemsSinglePossibleResult(self):
        response = self.app.get(ToDoAPITest.base_path + '/item?key=id&value=1')
        self.assertEqual('Shopping', response.json['title'])

    def test_getSelectedItemsMultipleResults(self):
        response = self.app.get(ToDoAPITest.base_path + '/items?key=title&value=light')
        self.assertEqual(2, len(response.json))

    def test_getSelectedItemsSingleResult(self):
        response = self.app.get(ToDoAPITest.base_path + '/items?key=title&value=Shopping')
        self.assertEqual(1, len(response.json))

    def test_getSelectedItemsInvalidKey(self):
        response = self.app.get(ToDoAPITest.base_path + '/items?key=invalid&value=Shopping')
        self.assertEqual('Database Error', response.json['message'])

    def test_getSingleItemsInvalidKey(self):
        response = self.app.get(ToDoAPITest.base_path + '/item?key=invalid&value=Shopping')
        self.assertEqual('Database Error', response.json['message'])
