# Credentials

----

> Credentials management features

> Package `anwdlclient.tools.credentials`

## Constants

None

## Classes

### `SessionCredentialsManager`

#### Definition

```
class SessionCredentialsManager(session_credentials_db_path: str)
```

> Provides session credentials storage and management functionality

_Parameters_ : 

- `session_credentials_db_path` : The session credentials database file path

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
	container_uuid,
	client_token
)
```

- `entry_id` : The entry ID
- `creation_timestamp` : The entry creation timestamp
- `server_ip` : The affiliated server IP
- `server_port` : The affiliated server port
- `container_uuid` : The container UUID
- `client_token` : The client token

---
```
addEntry(
	server_ip: str,
    server_port: int,
    container_uuid: str,
    client_token: str,
) -> tuple
```

> Add an entry

_Parameters_ : 

- `server_ip` : The server IP
- `server_port` : The server listen port
- `container_uuid` : The container UUID
- `client_token` : The client token

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

**NOTE** : Since the `container_uuid` and the `client_token` values are meant to be read and reused later, they are stored in plain text on the database.

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

### `ContainerCredentialsManager`

#### Definition

```
class ContainerCredentialsManager(container_credentials_db_path: str)
```

> Provides container credentials storage and management functionality

_Parameters_ : 

- `container_credentials_db_path` : The container credentials database file path

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
	container_username,
	container_password,
	container_listen_port
)
```

- `entry_id` : The entry ID
- `creation_timestamp` : The entry creation timestamp
- `server_ip` : The affiliated server IP
- `server_port` : The affiliated server port
- `container_username` : The container SSH username
- `container_password` : The container SSH password
- `container_listen_port` : The container SSH listen port

---
```
addEntry(
    server_ip: str,
    server_port: int,
    container_username: str,
    container_password: str,
    container_listen_port: int
) -> tuple
```

> Add an entry

_Parameters_ : 

- `server_ip` : The server IP
- `server_port` : The server listen port
- `container_username` : The container SSH username
- `container_password` : The container SSH password
- `container_listen_port` : The container SSH listen port

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

**NOTE** : Since the `container_username`, `container_password` and the `container_listen_port` values are meant to be read and reused later, they are stored in plain text on the database.

---
```
listEntries() -> list
```

> List entries

_Parameters_ : 

- None

_Return value_ : 

- A list of tuples representing every container credentials entries on the database : 

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