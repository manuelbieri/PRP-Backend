import abc
import unittest
import flask.testing

from testUtilities.databaseUtilities import *


class APITest(unittest.TestCase):
    base_path: str
    database_name: str = "test.db"
    path: str
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    @abc.abstractmethod
    def setUpDatabase(self) -> None:
        pass

    @abc.abstractmethod
    def setUpAPIClient(self) -> flask.testing.FlaskClient:
        pass

    @classmethod
    def setUpClass(cls) -> None:
        APITest.connection, APITest.cursor = setUpConnectionAndCursor(APITest.path)

    @classmethod
    def tearDownClass(cls) -> None:
        cleanUpDatabase(APITest.path, APITest.connection)

    def setUp(self) -> None:
        setUpData(APITest.connection, APITest.cursor)
        self.app: flask.testing.FlaskClient = self.setUpAPIClient()
        self.setUpDatabase()

    def tearDown(self) -> None:
        APITest.connection.commit()
        deleteTable(APITest.cursor)
