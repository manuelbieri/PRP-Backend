import abc
import os.path
import sqlite3
from typing import List

import database.IDatabase
import database.DatabaseUtilites as dataUt


class Database(database.IDatabase.IDatabase, abc.ABC):
    def __init__(self, database_name, table, path=None):
        self.database: sqlite3.Connection = self._setDatabase(database_name, path)
        self.table: str = self.setTable(table)
        self.database.row_factory = self._dictFactory
        self.cursor: sqlite3.Cursor = self.database.cursor()

    @staticmethod
    def _dictFactory(cursor, row):
        """
        Set a row factory to return a dict in search results.

        :param cursor: to set the factory for.
        :param row: to convert to a dict.
        :return: row as a dict.
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def _setDatabase(self, database_name, path=None) -> sqlite3.Connection:
        if path is None:
            path = os.path.join(os.path.dirname(__file__), "database", database_name)
        else:
            path = os.path.join(path, database_name)
        assert os.path.isfile(path)
        self.database = sqlite3.connect(path, check_same_thread=False)
        return self.database

    def setTable(self, table: str) -> str:
        assert table is not None
        self.table = table
        return table

    def getTables(self) -> List[dict]:
        return self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

    def readEntry(self, key: str, value) -> dict:
        assert key is not None
        assert value is not None

        result_cursor: sqlite3.Cursor = self._executeSearch(key, value)
        result = result_cursor.fetchone()
        result_cursor.close()
        if result is None:
            return {}

        assert len(result) == 3
        return result

    def _executeSearch(self, key, value) -> sqlite3.Cursor:
        operator = dataUt.parseOperator(value)
        value = dataUt.parseValue(value, search=True)
        return self.cursor.execute(
            f"""SELECT * FROM {self.table} WHERE {key}{operator}{value}""")

    def readEntries(self, key: str, value) -> List[dict]:
        assert key is not None
        assert value is not None
        result_cursor: sqlite3.Cursor = self._executeSearch(key, value)
        result = result_cursor.fetchall()
        if not result:
            return []
        assert len(result) > 0
        return result

    def readAllEntries(self) -> List[dict]:
        return self.cursor.execute(f"""SELECT * FROM {self.table}""").fetchall()

    def deleteEntry(self, entry_id: int) -> None:
        self.cursor.execute(f"""DELETE FROM items WHERE id={entry_id}""")
        self.database.commit()

    def closeDatabase(self) -> None:
        self.database.close()
