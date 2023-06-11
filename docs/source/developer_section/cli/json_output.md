# CLI JSON output

----

In order to communicate with other programs in an easy way, the Anweddol client CLI provides a JSON output feature that allows [inter-program communication](https://clig.dev/#simple-parts-that-work-together.

## Global structure

Each commands with the `--json` parameter results on a single JSON structure printed on `stdout` : 

```
{
	"status": STATUS
	"message": MESSAGE
	"data": DATA
}
```

- `STATUS` : The result status, it can be `"OK"` if there was no errors during the process, `"ERROR"` otherwise.
- `MESSAGE` : The message according to the command purpose.
- `DATA` : A dictionary containing every exploitable informations that a command can generate.

The `DATA` dictionary content changes according to the command context (see below).

**NOTE** : Configuration file related errors arent produced in a JSON format.

## Specific result JSON structures

### Catched exception

When an error occured during the process with any `--json` parameter set with subcommands, the output JSON will be : 

```
{
	"status": "ERROR",
	"message": "An error occured",
	"data": {
		"error": ERROR
	}
}
```

- `ERROR` : The error message that occured

### `create` sub-command

`anwdlclient create <ip>` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Container successfully created",
	"data": {
		"message": MESSAGE,
		SERVER_RESPONSE_DATA_DICTIONARY
	}
}
```

- `MESSAGE` : The received [response message](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#response-format)
- `SERVER_RESPONSE_DATA_DICTIONARY` : The `data` dictionary of the received request as described in the technical specifications [Communication section](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#response-format).

### `destroy` sub-command

`anwdlclient destroy <entry_id>` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Container successfully destroyed",
	"data": {
		"message": MESSAGE,
	}
}
```

- `MESSAGE` : The received [response message](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#response-format)

### `stat` sub-command

`anwdlclient stat <ip>` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Server statistics",
	"data": {
		"message": MESSAGE,
		SERVER_RESPONSE_DATA_DICTIONARY
	}
}
```

- `MESSAGE` : The received [response message](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#response-format)
- `SERVER_RESPONSE_DATA_DICTIONARY` : The `data` dictionary of the received request as described in the technical specifications [Communication section](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#response-format).

### `session` sub-command

`anwdlclient session -l` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Recorded entries ID",
	"data": {
		"entry_list": ENTRY_LIST
	}
}
```

- `ENTRY_LIST` : The recorded entries list

`anwdlclient session -p` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Entry ID content",
	"data": {
		"created": CREATION_TIMESTAMP,
        "server_ip": SERVER_IP,
        "server_port": SERVER_PORT,
        "container_uuid": CONTAINER_UUID,
        "client_token": CLIENT_TOKEN,
	}
}
```

- `CREATION_TIMESTAMP` : The entry creation timestamp
- `SERVER_IP` : The server IP
- `SERVER_PORT` : The server listen port
- `CONTAINER_UUID` : The container UUID
- `CLIENT_TOKEN` : The affiliated client token

`anwdlclient session -d` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Entry ID was deleted",
	"data": {}
}
```

### `container` sub-command

`anwdlclient container -l` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Recorded entries ID",
	"data": {
		"entry_list": ENTRY_LIST
	}
}
```

- `ENTRY_LIST` : The recorded entries list

`anwdlclient container -p` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Entry ID content",
	"data": {
		"created": CREATION_TIMESTAMP,
        "server_ip": SERVER_IP,
        "server_port": SERVER_PORT,
        "container_username": CONTAINER_USERNAME,
        "container_password": CONTAINER_PASSWORD,
        "container_listen_port": CONTAINER_LISTEN_PORT
	}
}
```

- `CREATION_TIMESTAMP` : The entry creation timestamp
- `SERVER_IP` : The server IP
- `SERVER_PORT` : The server listen port
- `CONTAINER_USERNAME` : The container SSH username
- `CONTAINER_PASSWORD` : The container SSH password
- `CONTAINER_LISTEN_PORT` : The container SSH listen port

`anwdlclient container -d` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Entry ID was deleted",
	"data": {}
}
```

### `access-tk` sub-command

`anwdlclient container -l` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Recorded entries ID",
	"data": {
		"entry_list": ENTRY_LIST
	}
}
```

- `ENTRY_LIST` : The recorded entries list

`anwdlclient container -a` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "New token entry created",
	"data": {
		"entry_id": ENTRY_ID
	}
}
```

- `ENTRY_ID` : The created entry ID

`anwdlclient container -p` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Entry ID content",
	"data": {
		"created": CREATION_TIMESTAMP,
        "server_ip": SERVER_IP,
        "server_port": SERVER_PORT,
        "access_token": ACCESS_TOKEN,
	}
}
```

- `CREATION_TIMESTAMP` : The entry creation timestamp
- `SERVER_IP` : The server IP
- `SERVER_PORT` : The server listen port
- `ACCESS_TOKEN` : The affiliated access_token

`anwdlclient container -d` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Entry ID was deleted",
	"data": {}
}
```

### `regen-rsa` sub-command

`anwdlclient regen-rsa` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "RSA keys re-generated",
	"data": {
		"fingerprint": FINGERPRINT
	}
}
```

- `FINGERPRINT` : The new generated public key's SHA256 digest