import os.path
from typing import List

import databaseTest.test_Database
import database.ToDoDatabase as dB


class TestToDoDatabase(databaseTest.test_Database.TestDatabase):
    def createDatabase(self) -> dB.ToDoDatabase:
        return dB.ToDoDatabase(TestToDoDatabase.database_name, "items", os.path.dirname(__file__))

    def setUp(self) -> None:
        self.setUpData()

    def test_write_new_entry(self):
        self.database.writeNewEntry({"title": "New Item", "description": "This is a new item."})
        result: List[dict] = self.database.readAllEntries()
        self.assertEqual(5, len(result))

    def test_write_new_entry_invalid_try(self):
        self.assertRaises(AssertionError, lambda: self.database.writeNewEntry(
            {"titles": "invalid item in dict", "description": "This is an invalid item."}))
        result: List[dict] = self.database.readAllEntries()
        self.assertEqual(4, len(result))

    def test_write_new_entries(self):
        self.database.writeNewEntries([{"title": "New Item 1", "description": "This is the first new item."},
                                       {"title": "New Item 2", "description": "This is the second new item."}])
        result: List[dict] = self.database.readAllEntries()
        self.assertEqual(6, len(result))

    def test_write_new_entries_containing_invalid_items(self):
        self.assertRaises(AssertionError, lambda: self.database.writeNewEntries(
            [{"title": "New Item 1", "description": "This is the first new item."},
             {"titles": "invalid item in dict", "description": "This is the invalid item."}]))
        result: List[dict] = self.database.readAllEntries()
        self.assertEqual(5, len(result))
