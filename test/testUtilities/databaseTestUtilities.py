import copy
import sqlite3
import os
from typing import List

import database.IDatabase

todoValues: List[dict] = [{'title': 'Shopping', 'description': 'Grocery Shopping'},
                          {'title': 'Lights', 'description': 'Lights for the dining room'},
                          {'title': 'Lights', 'description': 'Lights for the bathroom'},
                          {'title': 'Clean up', 'description': None}]


def addDataToTable(c: database.IDatabase.IDatabase, values: List[dict]):
    c.writeNewEntries(1, copy.deepcopy(values))
    c.writeNewEntries(2, copy.deepcopy(values))


def deleteDatabase(path: str):
    assert os.path.isfile(path)
    os.remove(path)


def createDatabaseFile(path):
    connection: sqlite3.Connection = sqlite3.connect(path)
    connection.close()
