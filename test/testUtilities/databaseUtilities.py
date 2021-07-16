import sqlite3
import os


def setUpConnectionAndCursor(path: str) -> (sqlite3.Connection, sqlite3.Cursor):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    return connection, cursor


def cleanUpDatabase(path: str, connection: sqlite3.Connection) -> None:
    connection.commit()
    connection.close()
    deleteDatabase(path)


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
