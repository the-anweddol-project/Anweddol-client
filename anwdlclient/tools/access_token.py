"""
Copyright 2023 The Anweddol project
See the LICENSE file for licensing informations
---

This module provides additional features for access token 
storage and management.

"""

from typing import Union
import sqlite3
import time

# Default parameters
DEFAULT_COMMIT = False


class AccessTokenManager:
    def __init__(self, access_token_db_path: str):
        self.database_connection = sqlite3.connect(
            access_token_db_path, check_same_thread=False
        )
        self.database_cursor = self.database_connection.cursor()
        self.is_closed = False

        self.database_cursor.execute(
            """CREATE TABLE IF NOT EXISTS AnweddolClientAccessTokenTable (
				EntryID INTEGER NOT NULL PRIMARY KEY, 
				CreationTimestamp INTEGER NOT NULL,
				ServerIP TEXT NOT NULL,
                ServerPort INTEGER NOT NULL,
				AccessToken TEXT NOT NULL
			)"""
        )

    def __del__(self):
        if not self.isClosed():
            self.closeDatabase()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if not self.isClosed():
            self.closeDatabase()

    def isClosed(self) -> bool:
        return self.is_closed

    def getDatabaseConnection(self) -> sqlite3.Connection:
        return self.database_connection

    def getCursor(self) -> sqlite3.Cursor:
        return self.database_cursor

    def getEntryID(self, server_ip: str) -> Union[None, int]:
        query_cursor = self.database_cursor.execute(
            "SELECT EntryID FROM AnweddolClientAccessTokenTable WHERE ServerIP=?",
            (server_ip,),
        )
        query_result = query_cursor.fetchone()

        return query_result[0] if query_result else None

    def getEntry(self, entry_id: int) -> tuple:
        query_cursor = self.database_cursor.execute(
            "SELECT * FROM AnweddolClientAccessTokenTable WHERE EntryID=?", (entry_id,)
        )

        return query_cursor.fetchone()

    def addEntry(self, server_ip: str, server_port: int, access_token: str) -> tuple:
        new_entry_creation_timestamp = int(time.time())

        self.database_cursor.execute(
            """INSERT INTO AnweddolClientAccessTokenTable (
                CreationTimestamp, 
                ServerIP, 
                ServerPort, 
                AccessToken) VALUES (?, ?, ?, ?)""",
            (new_entry_creation_timestamp, server_ip, server_port, access_token),
        )
        self.database_connection.commit()

        return (
            self.database_cursor.lastrowid,
            new_entry_creation_timestamp,
        )

    def executeQuery(
        self, text_query: str, parameters: tuple = (), commit: bool = DEFAULT_COMMIT
    ) -> sqlite3.Cursor:
        result = self.database_cursor.execute(text_query, parameters)

        if commit:
            self.database_connection.commit()

        return result

    def listEntries(self) -> list:
        query_cursor = self.database_cursor.execute(
            "SELECT EntryID, CreationTimestamp, ServerIP FROM AnweddolClientAccessTokenTable",
        )

        return query_cursor.fetchall()

    def deleteEntry(self, entry_id: int) -> None:
        self.database_cursor.execute(
            "DELETE FROM AnweddolClientAccessTokenTable WHERE EntryID=?",
            (entry_id,),
        )
        self.database_connection.commit()

    def closeDatabase(self) -> None:
        try:
            self.database_cursor.close()
            self.database_connection.close()

        except sqlite3.ProgrammingError:
            pass

        self.is_closed = True
