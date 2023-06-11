# Client
---

> Client management features

> Package `anwdlclient.core.client`

## Constants

Default values :

| Name                         | Value   | Description                                           |
| -------------------------  - | ------- | ----------------------------------------------------- |
| `DEFAULT_SERVER_LISTEN_PORT` | `6150`  | The default server listen port                        |
| `DEFAULT_CLIENT_TIMEOUT`     | `10`    | The default client timeout                            |
| `DEFAULT_AUTO_CONNECT`       | `True`  | Automatically connect to the server at initialization |
| `DEFAULT_RECEIVE_FIRST`      | `True`  | Receive the public key first by default               |

Constants definition :

| Name                           | Value                  | Definition                                                                 |
| ------------------------------ | ---------------------- | -------------------------------------------------------------------------- |
| `MESSAGE_OK`                   | `"1"`                  | Message used during key exchange to transmit a state or an acknowledgement |
| `MESSAGE_NOK`                  | `"0"`                  | Message used during key exchange to transmit a state or an acknowledgement |
| `REQUEST_VERB_CREATE`          | `"CREATE"`             | The verb indicating the intent to create a new container                   |
| `REQUEST_VERB_DESTROY`         | `"DESTROY"`            | The verb indicating the intent to destroy a container                      |
| `REQUEST_VERB_STAT`            | `"STAT"`               | The verb indicating the intent to get the server runtime statistics        |
| `RESPONSE_MSG_OK`              | `"OK"`                 | Message specifying that the request was correctly handled by the server    |
| `RESPONSE_MSG_BAD_AUTH`        | `"Bad authentication"` | Message specifying that invalid credentials were given to the server       |
| `RESPONSE_MSG_BAD_REQ`         | `"Bad request"`        | Message specifying that the received request is malformed                  |
| `RESPONSE_MSG_REFUSED_REQ`     | `"Refused request"`    | Message specifying that the received request was refused                   |
| `RESPONSE_MSG_UNAVAILABLE`     | `"Unavailable"`        | Message specifying that the server is currently unavailable                |
| `RESPONSE_MSG_INTERNAL_ERROR`  | `"Internal error"`     | Message specifying that the server experienced an internal error           |

## Classes

### `ClientInterface`

#### Definition

```
class ClientInterface(
	server_ip: str = None,
	server_listen_port: int = DEFAULT_SERVER_LISTEN_PORT,
	timeout: int = DEFAULT_CLIENT_TIMEOUT,
	rsa_wrapper: RSAWrapper = None,
	aes_wrapper: AESWrapper = None,
	auto_connect: bool = DEFAULT_AUTO_CONNECT,
)
```

> Represents a client to interact with servers

_Parameters_ :

- `server_ip` : The server IP to connect to
- `server_port` : The server listen port
- `timeout` : The timeout to set
- `rsa_wrapper` : The `RSAWrapper` instance that will be used on the client
- `aes_wrapper` : The `AESWrapper` instance that will be used on the client
- `auto_connect`: Automatically connect to the specified server coordinates

**NOTE** : The connection is automatically closed when the `__del__` method is called.

#### Methods

```
isClosed() -> bool
```

> Check if the client is closed or not

_Parameters_ : 

- None

_Return value_ :

- `True` if the client is closed, `False` otherwise

```
getSocketDescriptor() -> socket.socket
```

> Get the client socket descriptor

_Parameters_ :

- None

_Return value_ :

- The socket descriptor of the client

---

```
getRSAWrapper() -> RSAWrapper
```

> Get the client `RSAWrapper` instance

_Parameters_ :

- None

_Return value_:

- The `RSAWrapper` instance of the client

---

```
getAESWrapper() -> AESWrapper
```

> Get the client `AESWrapper` instance

_Parameters_ :

- None

_Return value_:

- The `AESWrapper` instance of the client

---

```
setRSAWrapper(rsa_wrapper: RSAWrapper) -> None
```

> Set the client `RSAWrapper` instance

_Parameters_ :

- `rsa_wrapper` : The `RSAWrapper` instance to set

_Return value_ :

- None

---

```
setAESWrapper(aes_wrapper: AESWrapper) -> None
```

> Set the client `AESWrapper` instance

_Parameters_ :

- `aes_wrapper` : The `AESWrapper` instance to set

_Return value_ :

- None

---

```
connectServer(receive_first: bool = DEFAULT_RECEIVE_FIRST) -> None
```

> Establish a connection with the server

_Paramaters_ : 

- `receive_first` : Receive the RSA and AES keys first

_Return value_ :

- None

_Possible raise classes_ :

- `RuntimeError`

**NOTE** : When this method is called, the RSA and AES keys will be automatically exchanged (see the technical specifications [Communication section](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#encryption)).

---

```
sendPublicRSAKey() -> None
```

> Send the local public RSA key

_Parameters_ :

- None

_Return value_ :

- None

_Possible raise classes_ :

- `RuntimeError`

---

```
recvPublicRSAKey() -> None
```

> Receive the client's public RSA key

_Parameters_ :

- None

_Return value_ :

- None

_Possible raise classes_ :

- `RuntimeError`
- `ValueError`

---

```
sendAESKey() -> None
```

> Send the local AES key

_Parameters_ :

- None

_Return value_ :

- None

_Possible raise classes_ :

- `RuntimeError`
- `ValueError`

---

```
recvAESKey() -> None
```

> Receive the local AES key

_Parameters_ :

- None

_Return value_ :

- None

_Possible raise classes_ :

- `RuntimeError`
- `ValueError`

---

```
sendRequest(verb: str, parameters: dict = {}) -> None
```

> Send a request to the server

_Parameters_ : 

- `verb` : The verb to send
- `parameters` : The parameters dictionary to send. The content must be an empty dict or a normalized [Request format](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#request-format) dictionary.

_Return value_ :

- None

_Possible raise classes_ :

- `ValueError`
- `RuntimeError`

---

```
recvResponse() -> dict
```

> Receive a response from the server

_Parameters_ :

- None

_Return value_ :

- The received response  as a normalized [Response format](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#response-format) dictionary

_Possible raise classes_ :

- `RuntimeError`
