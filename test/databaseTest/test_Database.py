import abc
import os.path
import sqlite3
import unittest
from typing import List

import database.IDatabase as dB


class TestDatabase(unittest.TestCase):
    database_name: str = "test.db"
    path = os.path.join(os.path.dirname(__file__), database_name)
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    @classmethod
    def setUpClass(cls) -> None:
        TestDatabase.connection = sqlite3.connect(TestDatabase.path)
        TestDatabase.cursor = TestDatabase.connection.cursor()

    @classmethod
    def tearDownClass(cls) -> None:
        TestDatabase.connection.commit()
        TestDatabase.connection.close()
        deleteDatabase(TestDatabase.path)

    def setUp(self) -> None:
        createTable(TestDatabase.cursor)
        addDataToTable(TestDatabase.cursor)
        TestDatabase.connection.commit()
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

    def test_write_new_entry(self):
        self.fail()

    def test_write_new_entries(self):
        self.fail()


def createTable(c: sqlite3.Cursor):
    query = """
            CREATE TABLE IF NOT EXISTS "items" (
                "id"	INTEGER,
                "title"	TEXT NOT NULL,
                "description"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            """
    c.execute(query)


def addDataToTable(c: sqlite3.Cursor):
    values = [("Shopping", "Grocery Shopping"),
              ("Lights", "Lights for the dining room"),
              ("Lights", "Lights for the bathroom"),
              ("Clean up", None)]
    try:
        c.executemany('INSERT INTO items(title, description) VALUES (?,?)', values)
    except sqlite3.IntegrityError:
        # data already inserted
        pass


def deleteTable(c: sqlite3.Cursor):
    c.execute("""DROP TABLE IF EXISTS items""")


def deleteDatabase(path: str):
    assert os.path.isfile(path)
    os.remove(path)
