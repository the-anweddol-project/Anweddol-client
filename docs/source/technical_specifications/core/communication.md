# Communication

---

## Format

Requests and responses sent between the client and the server are JSON structures : A widely used data format, cross-platform and easily manipulable.

Before sending anything, the size of the packet is sent in an 8 byte message, padded with `'='` characters : 

| Message         | Length        | Padded message length       |
| --------------- | ------------- | --------------------------- |
| `"hello world"` | 11 characters | `"11======"` (8 characters) |

Thus, the native theorical maximum packet size is 99 999 999 bytes.

## Request format

Here is a typical request structure that a client will send : 

```
{
	"verb": VERB;
	"parameters": PARAMETERS
}
```

- *VERB*

  Like an HTTP request, the verb depicts the action to execute on the server side. There is 3 natively supported verbs :

	- `"CREATE"`

	  Defines the intent to create a new container.

	- `"DESTROY"`

	  Defines the intent to destroy a previously created container.

	- `"STAT"`

	  Defines the intent to gather information about a server runtime.

  Note that a server implementation can handle custom verbs.

- *PARAMETERS*

  This is the section reserved for any kind of parameters used to provide additional information in a request.

## Response format

Here is a typical response structure that a client will receive : 

```
{
	"success": SUCCESS;
	"message": MESSAGE;
	"data": DATA
}
```

- *SUCCESS*
  
  Boolean value that defines the current state of the request processing on the server. `True` if the request was processed withour errors, `False` otherwise.

- *MESSAGE*

  The additional information coming along with the response. It can be anything that explains what happened on the server side if an error occured or not (see the 'Error handling' point below).

- *DATA*

  The data section, reserved for parameters returned by the server after the request processing.

## Error handling

When an error occurs during the processing of a request on the server side, a message is set in the response explaining what's wrong. 

Here is a non-exhaustive list of status codes and their messages : 

|Message                | Meaning                                      |
|---------------------- | -------------------------------------------- |
|`"OK"`                 | The request was successfully satisfied       |
|`"Bad authentication"` | The sender specified invalid credentials     |
|`"Bad request"`        | The previous request was malformed           |
|`"Refused request"`    | The request was refused                      |
|`"Unavailable"`        | The server is currently unavailable          |
|`"Internal error"`     | The server is experiencing an internal error |

Note that messages depicting an error may come with an additional explanation of why the error occurred : 

```
"Bad request (reason : Unsupported or unknown verb)"
```

## Security

### Encryption

For security and integrity reasons, requests and responses are encrypted in AES 256 CBC. Each AES key and Initialization Vectors are different for every session.

RSA keys length is 4096 bytes by default, they are used to send the session AES key to the client securely.

Here is a visual example of how the keys are exchanged with a client : 

> Bold text mean RSA encrypted text

> '>'/'<' symbol means 'send' and 'o' symbol means 'receive'

| A | packet content   | B |
|---|------------------|---|
|>  | connexion        |o  |
|>  | A RSA public key |o  |
|o  | validation       |<  |
|o  | B RSA public Key |<  |
|>  | validation       |o  |
|>  | **A AES Key**    |o  |
|o  | validation       |<  |
|o  | **B AES Key**    |<  |
|>  | validation       |o  | 

```{note}
Since the block size is limited to 512 bytes with default parameters for RSA instances, it is not suitable to send or receive data in a client/server communication context. That's why an AES cryptosystem implementation exists to fix the problem.
```

For security matters, the peer that sends a packet will also generate a new AES IV that will be appended to the encrypted JSON request message.

### Sanitization

Requests and responses are sanitized upon sending and receiving at each end.

Here are the raw [Cerberus](https://docs.python-cerberus.org/en/stable/index.html) validation schemes used to verify the format and content of requests and responses : 

#### Request cerberus validation scheme

```
{
    "verb": {
        "type": "string",
        "regex": r"^[A-Z]{1,}$",
        "required": True,
    },
    "parameters": {
        "type": "dict",
        "required": True,
        "schema": {
            "container_uuid": {
                "type": "string",
                "regex": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
                "required": False,
                "dependencies": ["client_token"],
            },
            "client_token": {
                "type": "string",
                "regex": r"^[0-9a-zA-Z-_]{255}$",
                "required": False,
                "dependencies": ["container_uuid"],
            },
        },
    },
}
```

#### Response cerberus validation scheme

```
{
    "success": {
        "type": "boolean",
        "required": True,
    },
    "message": {
        "type": "string",
        "required": True,
    },
    "data": {
        "type": "dict",
        "required": True,
        "schema": {
            "container_uuid": {
                "type": "string",
                "regex": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
                "required": False,
                "dependencies": [
                    "client_token",
                    "container_iso_sha256",
                    "container_username",
                    "container_password",
                    "container_listen_port",
                ],
            },
            "client_token": {
                "type": "string",
                "regex": r"^[0-9a-zA-Z-_]{255}$",
                "required": False,
                "dependencies": [
                    "container_uuid",
                    "container_iso_sha256",
                    "container_username",
                    "container_password",
                    "container_listen_port",
                ],
            },
            "container_iso_sha256": {
                "type": "string",
                "regex": r"^[a-f0-9]{64}$",
                "required": False,
                "dependencies": [
                    "container_uuid",
                    "client_token",
                    "container_username",
                    "container_password",
                    "container_listen_port",
                ],
            },
            "container_username": {
                "type": "string",
                "regex": r"^user_[0-9]{5}$",
                "required": False,
                "dependencies": [
                    "container_uuid",
                    "client_token",
                    "container_iso_sha256",
                    "container_password",
                    "container_listen_port",
                ],
            },
            "container_password": {
                "type": "string",
                "regex": r"^[a-zA-Z0-9]{1,}$",
                "required": False,
                "dependencies": [
                    "container_uuid",
                    "client_token",
                    "container_iso_sha256",
                    "container_username",
                    "container_listen_port",
                ],
            },
            "container_listen_port": {
                "type": "integer",
                "required": False,
                "min": 1,
                "max": 65535,
                "dependencies": [
                    "container_uuid",
                    "client_token",
                    "container_iso_sha256",
                    "container_username",
                    "container_password",
                ],
            },
            "uptime": {
                "type": "integer",
                "required": False,
                "dependencies": ["version"],
                "min": 0,
            },
            "version": {
                "type": "string",
                "required": False,
                "dependencies": ["uptime"],
            },
        },
    },
}
```