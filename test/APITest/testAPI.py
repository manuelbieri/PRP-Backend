import abc
import unittest
import flask.testing

import testUtilities.databaseTestUtilities as dataUt


class APITest(unittest.TestCase):
    api_base_path: str
    database_name: str = "test.db"
    path: str

    @abc.abstractmethod
    def setUpDatabase(self) -> None:
        pass

    @abc.abstractmethod
    def setUpAPIClient(self) -> flask.testing.FlaskClient:
        pass

    @classmethod
    def setUpClass(cls) -> None:
        dataUt.createDatabaseFile(APITest.path)

    @classmethod
    def tearDownClass(cls) -> None:
        dataUt.deleteDatabase(APITest.path)

    def setUp(self) -> None:
        self.setUpDatabase()
        self.app: flask.testing.FlaskClient = self.setUpAPIClient()

    @abc.abstractmethod
    def tearDown(self) -> None:
        pass
