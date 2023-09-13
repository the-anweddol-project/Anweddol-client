# CLI JSON output

----

In order to communicate with other programs in an easy way, the Anweddol client CLI provides a JSON output feature that allows [inter-program communication](https://clig.dev/#simple-parts-that-work-together.

## Global structure

Each commands with the `--json` parameter results on a single JSON structure printed on `stdout` : 

```
{
	"status": STATUS
	"message": MESSAGE
	"result": RESULT
}
```

- *STATUS*

  The result status, it can be `"OK"` if there was no errors during the process, `"ERROR"` otherwise.

- *MESSAGE*

  The message according to the state of the command purpose.

- *RESULT*

  A dictionary containing every exploitable informations that a command can generate.

The `RESULT` dictionary content changes according to the command context (see below).

```{note}
If a subcommand involves server interaction, the `message` and `data` response keys will be set in the JSON *RESULT* key.
```

```{warning}
Configuration file related errors arent produced in a JSON format.
```

## Specific result JSON structures

### Catched exception

When an error is raised during the process with any `--json` parameter set with subcommands, the output JSON will be : 

```
{
	"status": "ERROR",
	"message": "An error occured",
	"result": {
		"error": ERROR
	}
}
```

- *ERROR*

  The error class that was raised.

### `create` sub-command

`anwdlclient create <ip>` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Container successfully created",
	"result": {
		"message": MESSAGE,
		"data": DATA,
		"session_entry_id": SESSION_ENTRY_ID,
		"container_entry_id": CONTAINER_ENTRY_ID,
	}
}
```

- *MESSAGE*

  The received [response message](../../../technical_specifications/core/communication.md).

- *DATA*

  The `data` dictionary of the received request as described in the technical specifications [Communication section](../../../technical_specifications/core/communication.md).

- *SESSION_ENTRY_ID*

  The created session entry ID.

- *CONTAINER_ENTRY_ID*

  The created container entry ID.

If an error occurs in the process, the JSON structure will be :

```
{
	"status": "ERROR",
	"message": MESSAGE,
	"result": ERROR
}
```

- *MESSAGE*

  A specific message that describes the error.

- *ERROR*

  The data dictionary affiliated to the message content.

If the CLI received an invalid response from the server, `ERROR` will be :

```
{
	"error_dict": ERROR_DICT
}
```

- *ERROR_DICT*

  The dictionary depicting the errors detected in the response according to the [Cerberus](https://docs.python-cerberus.org/en/stable/errors.html) error format.

If the CLI received a response insinuating an error on the server side, `ERROR` will be :

```
{
	"response": RESPONSE
}
```

- *RESPONSE*

  The received response dictionary as described in the technical specifications [Communication section](../../../technical_specifications/core/communication.md).

### `destroy` sub-command

`anwdlclient destroy <entry_id>` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Container successfully destroyed",
	"result": {
		"message": MESSAGE,
	}
}
```

- *MESSAGE*

  The received [response message](../../../technical_specifications/core/communication.md).

If an error occurs in the process, the JSON structure will be :

```
{
	"status": "ERROR",
	"message": MESSAGE,
	"result": ERROR
}
```

- *MESSAGE*

  A specific message that describes the error.

- *ERROR*

  The data dictionary affiliated to the message content.

If the `<session_entry_id>` does not exists, `ERROR` will be an empty dictionary.

If the CLI received an invalid response from the server, `ERROR` will be :

```
{
	"error_dict": ERROR_DICT
}
```

- *ERROR_DICT*

  The dictionary depicting the errors detected in the response according to the [Cerberus](https://docs.python-cerberus.org/en/stable/errors.html) error format.

If the CLI received a response insinuating an error on the server side, `ERROR` will be :

```
{
	"response": RESPONSE
}
```

- *RESPONSE*

  The received response dictionary as described in the technical specifications [Communication section](../../../technical_specifications/core/communication.md).

### `stat` sub-command

`anwdlclient stat <ip>` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Server statistics",
	"result": {
		"message": MESSAGE,
		"data": DATA
	}
}
```

- *MESSAGE*

  The received [response message](../../../technical_specifications/core/communication.md).

- *DATA*

  The `data` dictionary of the received request as described in the technical specifications [Communication section](../../../technical_specifications/core/communication.md).

If an error occurs in the process, the JSON structure will be :

```
{
	"status": "ERROR",
	"message": MESSAGE,
	"result": DATA
}
```

- *MESSAGE*

  A specific message that describes the error.

- *DATA*

  The data dictionary affiliated to the message content.

If the CLI received an invalid response from the server, `DATA` will be :

```
{
	"error_dict": ERROR_DICT
}
```

- *ERROR_DICT*

  The dictionary depicting the errors detected in the response according to the [Cerberus](https://docs.python-cerberus.org/en/stable/errors.html) error format.

If the CLI received a response insinuating an error on the server side, `DATA` will be :

```
{
	"response": RESPONSE
}
```

- *RESPONSE*

  The received response dictionary as described in the technical specifications [Communication section](../../../technical_specifications/core/communication.md).

### `session` sub-command

`anwdlclient session -l` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Recorded entries ID",
	"result": {
		"entry_list": ENTRY_LIST
	}
}
```

- *ENTRY_LIST*

  The recorded entries list.

`anwdlclient session -p` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Entry ID content",
	"result": {
		"created": CREATION_TIMESTAMP,
        "server_ip": SERVER_IP,
        "server_port": SERVER_PORT,
        "container_uuid": CONTAINER_UUID,
        "client_token": CLIENT_TOKEN,
	}
}
```

- *CREATION_TIMESTAMP*

  The entry creation timestamp.

- *SERVER_IP*

  The server IP.

- *SERVER_PORT*

  The server listen port.

- *CONTAINER_UUID*

  The container UUID.

- *CLIENT_TOKEN*

  The affiliated client token.

`anwdlclient session -d` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Entry ID was deleted",
	"result": {}
}
```

If an error occurs in the process, the JSON structure will be :

```
{
	"status": "ERROR",
	"message": MESSAGE,
	"result": DATA
}
```

- *MESSAGE*

  A specific message that describes the error.

- *DATA*

  The data dictionary affiliated to the message content.

### `container` sub-command

`anwdlclient container -l` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Recorded entries ID",
	"result": {
		"entry_list": ENTRY_LIST
	}
}
```

- *ENTRY_LIST*

  The recorded entries list.

`anwdlclient container -p` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Entry ID content",
	"result": {
		"created": CREATION_TIMESTAMP,
        "server_ip": SERVER_IP,
        "server_port": SERVER_PORT,
        "container_username": CONTAINER_USERNAME,
        "container_password": CONTAINER_PASSWORD,
        "container_listen_port": CONTAINER_LISTEN_PORT
	}
}
```

- *CREATION_TIMESTAMP*

  The entry creation timestamp.

- *SERVER_IP*

  The server IP.

- *SERVER_PORT*

  The server listen port.

- *CONTAINER_USERNAME*

  The container SSH username.

- *CONTAINER_PASSWORD*

  The container SSH password.

- *CONTAINER_LISTEN_PORT*

  The container SSH listen port.

`anwdlclient container -d` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Entry ID was deleted",
	"result": {}
}
```

If an error occurs in the process, the JSON structure will be :

```
{
	"status": "ERROR",
	"message": MESSAGE,
	"result": DATA
}
```

- *MESSAGE*

  A specific message that describes the error.

- *DATA*

  The data dictionary affiliated to the message content.

### `access-tk` sub-command

`anwdlclient container -l` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Recorded entries ID",
	"result": {
		"entry_list": ENTRY_LIST
	}
}
```

- *ENTRY_LIST*

  The recorded entries list.

`anwdlclient container -a` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "New token entry created",
	"result": {
		"entry_id": ENTRY_ID
	}
}
```

- *ENTRY_ID*

  The created entry ID.

`anwdlclient container -p` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Entry ID content",
	"result": {
		"created": CREATION_TIMESTAMP,
        "server_ip": SERVER_IP,
        "server_port": SERVER_PORT,
        "access_token": ACCESS_TOKEN,
	}
}
```

- *CREATION_TIMESTAMP*

  The entry creation timestamp.

- *SERVER_IP*

  The server IP.

- *SERVER_PORT*

  The server listen port.

- *ACCESS_TOKEN*

  The affiliated access_token.

`anwdlclient container -d` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "Entry ID was deleted",
	"result": {}
}
```

If an error occurs in the process, the JSON structure will be :

```
{
	"status": "ERROR",
	"message": MESSAGE,
	"result": DATA
}
```

- *MESSAGE*

  A specific message that describes the error.

- *DATA*

  The data dictionary affiliated to the message content.

### `regen-rsa` sub-command

`anwdlclient regen-rsa` with the `--json` parameter will result in :

```
{
	"status": "OK",
	"message": "RSA keys re-generated",
	"result": {
		"fingerprint": FINGERPRINT
	}
}
```

- *FINGERPRINT*

  The new generated public key's SHA256 digest.