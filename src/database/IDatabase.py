import abc

from typing import List


"""Interface for database communication"""


class IDatabase(abc.ABC):
    @abc.abstractmethod
    def setTable(self, table: str) -> None:
        """
        Sets a new table to work with.

        :param table: to work with in consecutive commands.
        """

    @abc.abstractmethod
    def getTables(self) -> List[str]:
        """
        Returns list with all available tables in this database.

        :return: list with all available tables in this database.
        """

    @abc.abstractmethod
    def writeNewEntry(self, entry: dict) -> None:
        """
        Write a single entry into the database.

        :param entry: dict representing the entry to add.
        :return: true, whenever the adding of the entry was successful.
        """

    @abc.abstractmethod
    def writeNewEntries(self, entries: List[dict]) -> None:
        """
        Write multiple entries into the database.

        :param entries: list containing the entries represented by dicts.
        :return: true, whenever the adding of the entries was successful.
        """

    @abc.abstractmethod
    def readEntry(self, key: str, value) -> dict:
        """
        Reads an entry out of the database.

        :param key: category to search through.
        :param value: to match in the category.
        :return: the entry which matches the value in the category.
        """

    @abc.abstractmethod
    def readEntries(self, key: str, value) -> List[dict]:
        """
        Reads all matching entries out of the database.

        :param key: category to search through.
        :param value: to match in the category.
        :return: the entries which matches the value in the category.
        """

    @abc.abstractmethod
    def readAllEntries(self) -> List[dict]:
        """
        Reads all entries out of the database.

        :return: all entries in the database.
        """

    @abc.abstractmethod
    def updateEntry(self, entry_id: int, updated_values: dict) -> None:
        """
        Updates an entry with new values according to the id.

        :param entry_id: of the entry to update
        :param updated_values: to replace the old values with for the entry matching the id.
        """

    @abc.abstractmethod
    def deleteEntry(self, entry_id: int) -> None:
        """
        Deletes a matching entry from the database.

        :param entry_id: of the entry to delete.
        """

    @abc.abstractmethod
    def closeDatabase(self) -> None:
        """
        Closes the connection to this database.
        """

    @abc.abstractmethod
    def createDatabaseTables(self) -> None:
        """
        Creates the necessary tables for the database.
        """

    def cleanUpDatabase(self) -> None:
        """
        Cleans up all tables in the database.
        """
