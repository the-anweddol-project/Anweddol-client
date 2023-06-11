# Credentials storage

----

The Anweddol client `tools` features comes with a credentials storage facility (see the technical specifications [Authentication section](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/client_authentication.html) to learn more).

## Database

### Engine

This feature is using a SQLite file to store data, one file for each kind of credentials.

### Table representation

#### Session credentials

Here is a representation of the SQL table used to store [session credentials](https://anweddol-server.readthedocs.io/en/latest/technical_specifications/core/client_authentication.html#session-credentials) :

| EntryID                        | CreationTimestamp   | ServerIP        | ServerPort          | ContainerUUID      | ClientToken        |
|------------------------------- | ------------------- | --------------- | ------------------- | ------------------ | ------------------ |
| `INTEGER NOT NULL PRIMARY KEY` | `INTEGER NOT NULL`  | `TEXT NOT NULL` | `INTEGER NOT NULL`  | `TEXT NOT NULL`    | `TEXT NOT NULL`    |

- `EntryID` : Identifies the row
- `CreationTimestamp` : Store the row creation timestamp
- `ServerIP` : Store the affiliated server IP
- `ServerPort` : Store the affiliated server listen port
- `ContainerUUID` : Store the affiliated container UUID
- `ClientToken` : Store the affiliated client token

#### Container credentials

Here is a representation of the SQL table used to store [container credentials](https://anweddol-server.readthedocs.io/en/latest/technical_specifications/core/client_authentication.html#container-credentials) :

| EntryID                        | CreationTimestamp   | ServerIP        | ServerPort          | ContainerUsername  | ContainerPassword  | ContainerListenPort  |
|------------------------------- | ------------------- | --------------- | ------------------- | ------------------ | ------------------ | -------------------- |
| `INTEGER NOT NULL PRIMARY KEY` | `INTEGER NOT NULL`  | `TEXT NOT NULL` | `INTEGER NOT NULL`  | `TEXT NOT NULL`    | `TEXT NOT NULL`    | `INTEGER NOT NULL`   |

- `EntryID` : Identifies the row
- `CreationTimestamp` : Store the row creation timestamp
- `ServerIP` : Store the affiliated server IP
- `ServerPort` : Store the affiliated server listen port
- `ContainerUsername` : Store the affiliated container SSH username
- `ContainerPassword` : Store the affiliated container SSH password
- `ContainerListenPort` : Store the affiliated container SSH server listen port

### Security

Since those credentials are made to be read and exploited for further operations, every data is stored in plain text without specific encryption.