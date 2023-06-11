# Access token

----

An access token system is provided in the `tools` features.
It can be used by server implementations to restrict users of the service by providing tokens to authenticate them before processing the request.

A typical use case is when a client sends a request on a server, it must sends an access token in the request parameters that must match one of the tokens in the database in order to be processed by the server.

## Tokens

Tokens used are 124 characters url-safe strings.

## Database

### Engine

This feature is using a SQLite file to store data.

### Table representation

Here is a representation of the used SQL table :

| EntryID                        | CreationTimestamp   | ServerIP        | ServerPort         | AccessToken        |
|------------------------------- | ------------------- | --------------- | ------------------ | ------------------ |
| `INTEGER NOT NULL PRIMARY KEY` | `INTEGER NOT NULL`  | `TEXT NOT NULL` | `INTEGER NOT NULL` | `TEXT NOT NULL`    |

- `EntryID` : Identifies the row
- `CreationTimestamp` : Store the row creation timestamp
- `ServerIP` : Store the affiliated server IP
- `ServerPort` : Store the affiliated server listen port
- `AccessToken` : Store the affiliated access token

### Security

Since stored access tokens are made to be read and exploited for further operations, they are stored in plain text without specific encryption.