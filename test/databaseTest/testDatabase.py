import abc
import unittest
import os.path
from typing import List

import database.IDatabase as dB
import testUtilities.databaseTestUtilities as dataUt


class TestDatabase(unittest.TestCase):
    database_name: str = "test.db"
    path: str = os.path.join(os.path.dirname(__file__), database_name)

    @classmethod
    def setUpClass(cls) -> None:
        dataUt.createDatabaseFile(TestDatabase.path)

    @classmethod
    def tearDownClass(cls) -> None:
        dataUt.deleteDatabase(TestDatabase.path)

    def setUp(self) -> None:
        self.skipTest("Abstract test class")
        self.database: dB.IDatabase = dB.IDatabase()

    def tearDown(self) -> None:
        self.database.cleanUpDatabase()

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
