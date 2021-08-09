import abc
import unittest
from typing import List

import database.IDatabase as dB
from testUtilities.databaseUtilities import *


class TestDatabase(unittest.TestCase):
    database_name: str = "test.db"
    path: str = os.path.join(os.path.dirname(__file__), database_name)
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    @classmethod
    def setUpClass(cls) -> None:
        TestDatabase.connection, TestDatabase.cursor = setUpConnectionAndCursor(TestDatabase.path)

    @classmethod
    def tearDownClass(cls) -> None:
        cleanUpDatabase(TestDatabase.path, TestDatabase.connection)

    def setUp(self) -> None:
        self.skipTest("Abstract test class")

    def setUpData(self):
        setUpData(TestDatabase.connection, TestDatabase.cursor)
        self.database: dB.IDatabase = self.createDatabase()

    def tearDown(self) -> None:
        TestDatabase.connection.commit()
        deleteTable(TestDatabase.cursor)

    @abc.abstractmethod
    def createDatabase(self) -> dB.IDatabase:
        pass

    def test_get_tables(self):
        tables: List[str] = self.database.getTables()
        self.assertTrue({'name': 'items'} in tables)

    def test_read_entry(self):
        result = self.database.readEntry("id", 1)
        self.assertEqual(3, len(result))
        self.assertEqual(1, result["id"])

    def test_read_entry_no_results(self):
        result = self.database.readEntry("title", "not available")
        self.assertEqual(0, len(result))

    def test_read_entry_multiple_results(self):
        result = self.database.readEntry("title", "igh")
        self.assertEqual(3, len(result))

    def test_read_entries_one_result(self):
        result = self.database.readEntries("title", "Shopping")
        self.assertEqual(1, len(result))

    def test_read_entries_no_results(self):
        result = self.database.readEntries("title", "not available")
        self.assertEqual(0, len(result))

    def test_read_entries_multiple_results(self):
        result = self.database.readEntries("title", "Lights")
        self.assertEqual(2, len(result))

    @abc.abstractmethod
    def test_write_new_entry(self):
        pass

    @abc.abstractmethod
    def test_write_new_entries(self):
        pass

    def test_delete_entry(self):
        self.database.deleteEntry(1)
        result = self.database.readEntry("id", 1)
        self.assertEqual({}, result)