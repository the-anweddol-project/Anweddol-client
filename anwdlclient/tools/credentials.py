"""
Copyright 2023 The Anweddol project
See the LICENSE file for licensing informations
---

This module provides additional features for session and
container credentials storage and management.

"""

from typing import Union
import sqlite3
import time

# Default parameters
DEFAULT_COMMIT = False


# Since the two kinds of credentials are separated, there is one class for one database
class SessionCredentialsManager:
    def __init__(self, session_credentials_db_path: str):
        self.database_connection = sqlite3.connect(
            session_credentials_db_path, check_same_thread=False
        )
        self.database_cursor = self.database_connection.cursor()
        self.is_closed = False

        self.database_cursor.execute(
            """CREATE TABLE IF NOT EXISTS AnweddolClientSessionCredentialsTable (
                EntryID INTEGER NOT NULL PRIMARY KEY,
                CreationTimestamp INTEGER NOT NULL,
                ServerIP TEXT NOT NULL,
                ServerPort INTEGER NOT NULL,
                ContainerUUID TEXT NOT NULL,
                ClientToken TEXT NOT NULL
            )"""
        )

    def __del__(self):
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
            "SELECT EntryID FROM AnweddolClientSessionCredentialsTable WHERE ServerIP=?",
            (server_ip,),
        )
        query_result = query_cursor.fetchone()

        return query_result[0] if query_result else None

    def getEntry(self, entry_id: int) -> tuple:
        query_cursor = self.database_cursor.execute(
            "SELECT * FROM AnweddolClientSessionCredentialsTable WHERE EntryID=?",
            (entry_id,),
        )

        return query_cursor.fetchone()

    def addEntry(
        self, server_ip: str, server_port: int, container_uuid: str, client_token: str
    ) -> tuple:
        new_entry_creation_timestamp = int(time.time())

        self.database_cursor.execute(
            """INSERT INTO AnweddolClientSessionCredentialsTable (
                CreationTimestamp, 
                ServerIP, 
                ServerPort, 
                ContainerUUID, 
                ClientToken) VALUES (?, ?, ?, ?, ?)""",
            (
                new_entry_creation_timestamp,
                server_ip,
                server_port,
                container_uuid,
                client_token,
            ),
        )
        self.database_connection.commit()

        return (self.database_cursor.lastrowid, new_entry_creation_timestamp)

    def executeQuery(
        self, text_query: str, parameters: tuple = (), commit: bool = DEFAULT_COMMIT
    ) -> sqlite3.Cursor:
        result = self.database_cursor.execute(text_query, parameters)

        if commit:
            self.database_connection.commit()

        return result

    def listEntries(self) -> list:
        query_cursor = self.database_cursor.execute(
            "SELECT EntryID, CreationTimestamp, ServerIP FROM AnweddolClientSessionCredentialsTable",
        )

        return query_cursor.fetchall()

    def deleteEntry(self, entry_id: int) -> None:
        self.database_cursor.execute(
            "DELETE FROM AnweddolClientSessionCredentialsTable WHERE EntryID=?",
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


class ContainerCredentialsManager:
    def __init__(self, container_credentials_db_path: str):
        self.database_connection = sqlite3.connect(
            container_credentials_db_path, check_same_thread=False
        )
        self.database_cursor = self.database_connection.cursor()
        self.is_closed = False

        self.database_cursor.execute(
            """CREATE TABLE IF NOT EXISTS AnweddolClientContainerCredentialsTable (
                EntryID INTEGER NOT NULL PRIMARY KEY,
                CreationTimestamp INTEGER NOT NULL,
                ServerIP TEXT NOT NULL,
                ServerPort INTEGER NOT NULL,
                ContainerUsername TEXT NOT NULL,
                ContainerPassword TEXT NOT NULL,
                ContainerListenPort INTEGER NOT NULL
            )"""
        )

    def __del__(self):
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
            "SELECT EntryID FROM AnweddolClientContainerCredentialsTable WHERE ServerIP=?",
            (server_ip,),
        )
        query_result = query_cursor.fetchone()

        return query_result[0] if query_result else None

    def getEntry(self, entry_id: int) -> tuple:
        query_cursor = self.database_cursor.execute(
            "SELECT * FROM AnweddolClientContainerCredentialsTable WHERE EntryID=?",
            (entry_id,),
        )

        return query_cursor.fetchone()

    def addEntry(
        self,
        server_ip: str,
        server_port: int,
        container_username: str,
        container_password: str,
        container_listen_port: int,
    ) -> tuple:
        new_entry_creation_timestamp = int(time.time())

        self.database_cursor.execute(
            """INSERT INTO AnweddolClientContainerCredentialsTable (
                CreationTimestamp, 
                ServerIP, 
                ServerPort,
                ContainerUsername, 
                ContainerPassword, 
                ContainerListenPort) VALUES (?, ?, ?, ?, ?, ?)""",
            (
                new_entry_creation_timestamp,
                server_ip,
                server_port,
                container_username,
                container_password,
                container_listen_port,
            ),
        )
        self.database_connection.commit()

        return (self.database_cursor.lastrowid, new_entry_creation_timestamp)

    def executeQuery(
        self, text_query: str, parameters: tuple = (), commit: bool = DEFAULT_COMMIT
    ) -> sqlite3.Cursor:
        result = self.database_cursor.execute(text_query, parameters)

        if commit:
            self.database_connection.commit()

        return result

    def listEntries(self) -> list:
        query_cursor = self.database_cursor.execute(
            "SELECT EntryID, CreationTimestamp, ServerIP FROM AnweddolClientContainerCredentialsTable",
        )

        return query_cursor.fetchall()

    def deleteEntry(self, entry_id: int) -> None:
        self.database_cursor.execute(
            "DELETE FROM AnweddolClientContainerCredentialsTable WHERE EntryID=?",
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
