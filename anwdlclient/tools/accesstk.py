import sqlite3
import time


class AccessTokenManager:
    def __init__(self, access_token_db_path: str):
        self.database_connection = sqlite3.connect(
            access_token_db_path, check_same_thread=False
        )
        self.database_cursor = self.database_connection.cursor()

        self.database_cursor.execute(
            """CREATE TABLE IF NOT EXISTS AnweddolAccessTokenTable (
				EntryID INTEGER NOT NULL PRIMARY KEY, 
				CreationTimestamp INTEGER NOT NULL,
				ServerIP TEXT NOT NULL,
                ServerPort INTEGER NOT NULL,
				AccessToken TEXT NOT NULL
			)"""
        )

    def __del__(self):
        self.closeDatabase()

    def getDatabaseConnection(self) -> sqlite3.Connection:
        return self.database_connection

    def getCursor(self) -> sqlite3.Cursor:
        return self.database_cursor

    def getEntryID(self, server_ip: str) -> None | int:
        query_cursor = self.database_cursor.execute(
            "SELECT EntryID from AnweddolAccessTokenTable WHERE ServerIP=?",
            (server_ip,),
        )
        query_result = query_cursor.fetchone()

        return query_result[0] if query_result else None

    def getEntry(self, entry_id: int) -> tuple:
        query_cursor = self.database_cursor.execute(
            "SELECT * from AnweddolAccessTokenTable WHERE EntryID=?", (entry_id,)
        )

        return query_cursor.fetchone()

    def addEntry(self, server_ip: str, server_port: int, access_token: str) -> tuple:
        new_entry_creation_timestamp = int(time.time())

        try:
            self.database_cursor.execute(
                """INSERT INTO AnweddolAccessTokenTable (
                    CreationTimestamp, 
                    ServerIP, 
                    ServerPort, 
                    AccessToken) VALUES (?, ?, ?, ?)""",
                (new_entry_creation_timestamp, server_ip, server_port, access_token),
            )
            self.database_connection.commit()

        except Exception as E:
            self.database_connection.rollback()
            raise E

        return (
            self.database_cursor.lastrowid,
            new_entry_creation_timestamp,
        )

    def listEntries(self) -> list:
        query_cursor = self.database_cursor.execute(
            "SELECT EntryID, CreationTimestamp, ServerIP from AnweddolAccessTokenTable",
        )

        return query_cursor.fetchall()

    def deleteEntry(self, entry_id: int) -> None:
        try:
            self.database_cursor.execute(
                "DELETE from AnweddolAccessTokenTable WHERE EntryID=?",
                (entry_id,),
            )
            self.database_connection.commit()

        except Exception as E:
            self.database_connection.rollback()
            raise E

    def closeDatabase(self) -> None:
        try:
            self.database_cursor.close()
            self.database_connection.close()
        except sqlite3.ProgrammingError:
            pass
