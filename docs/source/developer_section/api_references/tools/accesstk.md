# Access token

----

## Constants

None

## Classes

### `AccessTokenManager`

#### Definition

```
class AccessTokenManager(access_token_db_path: str)
```

> Provides access token storage and management functionnality

_Parameters_ : 

- `access_token_db_path` : The access token database file path

#### Methods

```
getDatabaseConnection() -> sqlite3.Connection
```

> Get the [`sqlite3.Connection`](https://docs.python.org/3.8/library/sqlite3.html#sqlite3.Connection) object of the instance

_Parameters_ : 

- None

_Return value_ : 

- The `sqlite3.Connection` object of the instance

---
```
getCursor() -> sqlite3.Cursor:
```

> Get the [`sqlite3.Cursor`](https://docs.python.org/3.8/library/sqlite3.html#sqlite3.Cursor) object of the instance

_Parameters_ : 

- None

_Return value_ : 

- The `sqlite3.Cursor` object of the instance

---
```
getEntryID(server_ip: str) -> None | int
```

> Get the entry ID of a specific IP

_Parameters_ : 

- `server_ip` : The server IP to search for

_Return value_ : 

- The entry ID of the specified IP if exists, `None` otherwise. 

---
```
getEntry(entry_id: int) -> tuple
```

> Get entry credentials

_Parameters_ : 

- `entry_id` : The entry ID to get the credentials from

_Return value_ : 

- A tuple representing the full entry row : 

```
(
	entry_id,
	creation_timestamp,
	server_ip,
	server_port,
	access_token
)
```

- `entry_id` : The entry ID
- `creation_timestamp` : The entry creation timestamp
- `server_ip` : The affiliated server IP
- `server_port` : The affiliated server port
- `access_token` : The access token, in plain text

---
```
addEntry(
    server_ip: str,
    server_port: int,
    access_token: str,
) -> tuple
```

> Add an entry

_Parameters_ : 

- `server_ip` : The server IP
- `server_port` : The server listen port
- `access_token` : The access token

_Return value_ : 

- A tuple representing the infomations of the created entry :

```
(
	entry_id,
	creation_timestamp
)
```

- `entry_id` : The new entry ID
- `creation_timestamp` : The entry ID creation timestamp

**NOTE** : Since the `access_token` value is meant to be read and reused later, it is stored in plain text on the database.

---
```
listEntries() -> list
```

> List entries

_Parameters_ : 

- None

_Return value_ : 

- A list of tuples representing every session credentials entries on the database : 

```
(
	entry_id,
	creation_timestamp,
	server_ip
)
```

- `entry_id` : The entry ID
- `creation_timestamp` : The entry creation timestamp
- `server_ip` : The affiliated server IP

**NOTE** : Sensitive credentials arent listed with this method. Use the `getEntry` method to do so.

---
```
deleteEntry(entry_id: int) -> None
```

> Delete an entry

_Parameters_ : 

- `entry_id` : The entry ID to delete on the database

_Return value_ : 

- None

---
```
closeDatabase() -> None
```

> Close the database

_Parameters_ :

- None

_Return value_ :

- None

**NOTE** : This method is automatically called within the `__del__` method, but it is programatically better to call it naturally