from typing import List

import database.DatabaseUtilites as dataUt
import database.Database


class ToDoDatabase(database.Database.Database):
    def __init__(self, database_name, table, path=None):
        super().__init__(database_name, table, path)

    def updateEntry(self, entry_id: int, updated_values: dict) -> None:
        assert entry_id > 0
        assert updated_values is not None
        assert len(updated_values) == 2
        title: str = dataUt.parseValue(updated_values['title'])
        description: str = dataUt.parseValue(updated_values['description'])
        self.cursor.execute(f"""UPDATE items SET title = {title}, description = {description} WHERE id={entry_id}""")
        self.database.commit()

    def writeNewEntry(self, user_id: int, entry: dict) -> None:
        assert len(entry) > 0
        assert user_id > 0
        assert "title" in entry
        assert entry["title"] is not None
        entry["title"] = dataUt.parseValue(entry["title"])
        entry["description"] = dataUt.parseValue(entry["description"])
        self._insertRow(user_id, entry)
        self.database.commit()

    def writeNewEntries(self, user_id: int, entries: List[dict]) -> None:
        assert len(entries) > 0
        for entry in entries:
            self.writeNewEntry(user_id, entry)

    def _insertRow(self, user_id: int, entry: dict) -> None:
        self.cursor.execute(f"""INSERT INTO items(title,description,user) VALUES({entry["title"]},{entry["description"]},{user_id})""")

    def createDatabaseTables(self) -> None:
        query = """
                CREATE TABLE IF NOT EXISTS "items" (
                    "id"	INTEGER,
                    "title"	TEXT NOT NULL,
                    "description"	TEXT,
                    "user" INTEGER NOT NULL , 
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
                """
        self.cursor.execute(query)
