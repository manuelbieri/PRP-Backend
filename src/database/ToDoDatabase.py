from typing import List
import database.Database


class ToDoDatabase(database.Database.Database):
    def __init__(self, database_name, table, path=None):
        super().__init__(database_name, table, path)

    def updateEntry(self, entry_id: int, updated_values: dict) -> None:
        assert entry_id > 0
        assert updated_values is not None
        assert len(updated_values) == 2
        title: str = self._parseValue(updated_values['title'])
        description: str = self._parseValue(updated_values['description'])
        self.cursor.execute("""UPDATE items SET title = {title}, description = {description} WHERE id={id}"""
                            .format(title=title, description=description, id=entry_id))
        self.database.commit()

    def writeNewEntry(self, entry: dict) -> None:
        assert len(entry) > 0
        assert "title" in entry
        assert entry["title"] is not None
        entry["title"] = self._parseValue(entry["title"])
        entry["description"] = self._parseValue(entry["description"])
        self._insertRow(entry)
        self.database.commit()

    def writeNewEntries(self, entries: List[dict]) -> None:
        assert len(entries) > 0
        for entry in entries:
            self.writeNewEntry(entry)

    def _insertRow(self, entry: dict) -> None:
        self.cursor.execute("""INSERT INTO items(title,description) VALUES({title},{description})""".format(table=self.table, title=entry["title"], description=entry["description"]))
