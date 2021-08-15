import os
import sqlite3
import passlib.hash as passlib

import customExceptions.Exceptions
import database.DatabaseUtilites as dataUt


class UserHandler:
    def __init__(self, path: str = None):
        path = os.path.dirname(__file__) + "/users/users.db" if path is None else path + "/users.db"
        self.users: sqlite3.Connection = sqlite3.connect(path)
        self.cursor: sqlite3.Cursor = self.users.cursor()

    def closeHandler(self) -> None:
        self.users.close()
        del self

    def _createUserTable(self) -> None:
        query = """
                CREATE TABLE IF NOT EXISTS "users" (
                    "id"	INTEGER,
                    "name"	TEXT NOT NULL,
                    "password"	TEXT NOT NULL,
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
                """
        self.cursor.execute(query)
        self.users.commit()

    def addUser(self, user_id: str, password: str) -> None:
        assert user_id is not None and password is not None
        assert len(password) >= 8
        password_hash = passlib.pbkdf2_sha256.hash(password)
        password_hash = dataUt.parseValue(password_hash)
        user_id = dataUt.parseValue(user_id)
        self.cursor.execute(f"""INSERT INTO users(name, password) VALUES({user_id},{password_hash})""")
        self.users.commit()

    def getUserId(self, username: str) -> int:
        assert username is not None
        try:
            username = dataUt.parseValue(username)
            user_id: int = self.cursor.execute("""SELECT id FROM users WHERE name={username}""".format(username=username)).fetchone()[0]
            assert user_id > 0
            return user_id
        except TypeError:
            raise customExceptions.Exceptions.InvalidUser("Not an existing username")

    def checkPassword(self, username: str, password: str) -> bool:
        assert username is not None
        assert password is not None
        username = dataUt.parseValue(username)
        password_hash: str = self.cursor.execute("""SELECT password FROM users WHERE name={username}""".format(username=username)).fetchone()[0]
        return passlib.pbkdf2_sha256.verify(password, password_hash)
