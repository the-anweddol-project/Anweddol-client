# Client

---

## Constants

In the module `anwdlclient.core.client` :

### Default values

Constant name                 | Value   | Definition
----------------------------- | ------- | ----------
*DEFAULT_SERVER_LISTEN_PORT*  | 6150    | The default server listen port.
*DEFAULT_CLIENT_TIMEOUT*      | `None`  | The default client timeout.
*DEFAULT_RECEIVE_FIRST*       | `False` | Receive the keys first by default or not.

### Parameters

Constant name           | Value  | Definition
----------------------- | ------ | ----------
*MESSAGE_OK*            | `"1"`  | A simple message used in key exchange process, allowing client and server to communicate a successful action on their end. 
*MESSAGE_NOK*           | `"0"`  | A simple message used in key exchange process, allowing client and server to communicate an unsuccessful action on their end. 

### Request constants

Constant name                 | Value       | Definition
----------------------------- | ----------- | ----------
*REQUEST_VERB_CREATE*         | `"CREATE"`  | Identifies a CREATE request.
*REQUEST_VERB_DESTROY*        | `"DESTROY"` | Identifies a DESTROY request.
*REQUEST_VERB_STAT*           | `"STAT"`    | Identifies a STAT request.

### Response constants

Constant name                 | Value                  | Definition
----------------------------- | ---------------------- | ----------
*RESPONSE_MSG_OK*             | `"OK"`                 | A response message announcing a success.
*RESPONSE_MSG_BAD_AUTH*       | `"Bad authentication"` | A response message announcing an authentication error.
*RESPONSE_MSG_BAD_REQ*        | `"Bad request"`        | A response message announcing that a bad request was received.
*RESPONSE_MSG_REFUSED_REQ*    | `"Refused request"`    | A response message announcing that the request was refused.
*RESPONSE_MSG_UNAVAILABLE*    | `"Unavailable"`        | A response message announcing an unavailable service.
*RESPONSE_MSG_UNSPECIFIED*    | `"Unspecified"`        | A response message announcing an unspecified error or information.
*RESPONSE_MSG_INTERNAL_ERROR* | `"Internal error"`     | A response message announcing that an internal error occured during the request processing.

## class *ClientInterface*

### Definition

```{class} anwdlclient.core.client.ClientInterface(server_ip, server_listen_port, timeout, rsa_wrapper, aes_wrapper)
```

Represents a client to interact with servers.

**Parameters** :

> ```{attribute} server_ip
> Type : str
> 
> The server IP to connect to. Must be an IPv4 format.
> ```

> ```{attribute} server_listen_port
> Type : int
> 
> The remote server listen port. Default is `6150`.
> ```

> ```{attribute} timeout
> Type : int | `NoneType`
> 
> The timeout to set on the client socket. Defauls is `None`.
> ```

> ```{attribute} rsa_wrapper
> Type : `RSAWrapper` | `NoneType`
> 
> The `RSAWrapper` instance that will be used on the client. Default is `None`
> ```

> ```{attribute} aes_wrapper
> Type : `AESWrapper` | `NoneType`
> 
> The `AESWrapper` instance that will be used on the client. Default is `None`
> ```

```{tip}
This class can be used in a 'with' statement.
```

```{note}
The connection is closed with the `closeConnection()` method when the `__del__` method is called.

If the parameters `rsa_wrapper` or `aes_wrapper` are set to `None`, a new RSA or AES wrapper instance will be initialized.
```

### Methods

```{classmethod} isClosed()
```

Check if the client socket is closed or not.

**Parameters** : 

> None

**Return value** :

> Type : bool
>
> `True` if the client socket is closed, `False` otherwise.

---

```{classmethod} getSocketDescriptor()
```

Get the client socket descriptor

**Parameters** :

> None.

*Return value* :

> Type : [`socket.socket`](https://docs.python.org/3/library/socket.html#socket.socket)
>
> The socket descriptor of the client.

---

```{classmethod} getRSAWrapper()
```

Get the client `RSAWrapper` instance.

**Parameters** :

> None.

**Return value**:

> Type : `RSAWrapper`
>
> The `RSAWrapper` instance of the client.

---

```{classmethod} getAESWrapper()
```

Get the client `AESWrapper` instance.

**Parameters** :

> None.

**Return value**:

> Type : `AESWrapper`
>
> The `AESWrapper` instance of the client.

---

```{classmethod} setRSAWrapper(rsa_wrapper)
```

Set the client `RSAWrapper` instance.

**Parameters** :

> ```{attribute} rsa_wrapper
> Type : `RSAWrapper`
> 
> The `RSAWrapper` instance to set.
> ```

**Return value** :

> `None`.

---

```{classmethod} setAESWrapper(aes_wrapper)
```

Set the client `AESWrapper` instance.

**Parameters** :

> ```{attribute} aes_wrapper
> Type : `AESWrapper`
> 
> The `AESWrapper` instance to set.
> ```

**Return value** :

> `None`.

---

```{classmethod} connectServer(receive_first)
```

Establish a connection with the server.

**Paramaters** : 

> ```{attribute} receive_first
> Type : bool
> 
> `True` to receive the RSA and AES keys first, `False` otherwise. Default is `False`.
> ```

**Return value** :

> `None`.

**Possible raise classes** :

> ```{exception} RuntimeError
> An error occured due to a failed internal action.
>
> Raised in this method if the client is already connected.
> ```

```{note}
When this method is called, the RSA and AES keys will be automatically exchanged (see the technical specifications [Communication section](../../../technical_specifications/core/communication.md) to learn more).
```

---

```{classmethod} sendPublicRSAKey()
```

Send the local public RSA key.

**Parameters** :

> None.

**Return value** :

> `None`.

**Possible raise classes** :

> ```{exception} RuntimeError
> An error occured due to a failed internal action.
> 
> Raised in this method if the client is closed, or that the server refused the sent packet or the RSA key.
> ```

---

```{classmethod} recvPublicRSAKey()
```

Receive the server public RSA key.

**Parameters** :

> None.

**Return value** :

> `None`.

**Possible raise classes** :

> ```{exception} ValueError
> An error occured due to an invalid value set before or during the method call.
> 
> Raised in this method if an invalid key length has been received from the server.
> ```

> ```{exception} RuntimeError
> An error occured due to a failed internal action.
> 
> Raised in this method if the client is not connected to the server.
> ```

---

```{classmethod} sendAESKey()
```

Send the local AES key to the server.

**Parameters** :

> None.

**Return value** :

> `None`.

**Possible raise classes** :

> ```{exception} RuntimeError
> An error occured due to a failed internal action.
> 
> Raised in this method if the client is not connected to the server.
> ```

---

```{classmethod} recvAESKey()
```

Receive the AES key from the server.

**Parameters** :

> None

**Return value** :

> `None`.

**Possible raise classes** :

> ```{exception} RuntimeError
> An error occured due to a failed internal action.
> 
> Raised in this method if the client is not connected to the server.
> ```

---

```{classmethod} sendRequest(verb, parameters)
```

Send a request to the server.

**Parameters** : 

> ```{attribute} verb
> Type : str
> 
> The verb to send.
> ```

> ```{attribute} parameters
> Type : dict
> 
> The parameters dictionary to send. The content must be an empty dict or a normalized [Request format](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#request-format) dictionary. Default is an empty dict.
> ```

**Return value** :

> `None`.

**Possible raise classes** :

> ```{exception} ValueError
> An error occured due to an invalid value set before or during the method call.
> 
> Raised in this method if the specified values are invalid.
> ```

> ```{exception} RuntimeError
> An error occured due to a failed internal action.
> 
> Raised in this method if the client is not connected to the server.
> ```

---

```{classmethod} recvResponse()
```

Receive a response from the server.

**Parameters** :

> None.

**Return value** :

> Type : tuple
>
> A tuple representing the return value of the `verifyResponseContent` function :
> 
> ```
> (
> 	is_response_format_valid,
> 	sanitized_response_dictionary,
>   errors_dictionary,
> )
> ```
>
> - *is_response_format_valid*
>
>	Type : bool
> 
>   `True` if the response dictionary format is valid, `False` otherwise.
>
> - *sanitized_response_dictionary*
>
>	Type : dict
> 
>   The sanitized response as a normalized [Request format](../../../technical_specifications/core/communication.md) dictionary. `None` if `is_response_format_valid` is set to `False`.
> 
> - *errors_dictionary*
>
>	Type : dict
> 
>   A dictionary depicting the errors detected in the received request according to the [Cerberus](https://docs.python-cerberus.org/en/stable/errors.html) error format. `None` if `is_response_format_valid` is set to `True`.

**Possible raise classes** :

> ```{exception} ValueError
> An error occured due to an invalid value set before or during the method call.
> 
> Raised in this method if an invalid packet length has been received from the server.
> ```

> ```{exception} RuntimeError
> An error occured due to a failed internal action.
> 
> Raised in this method if the client is not connected to the server.
> ```

### Undocumented methods

- `__del__()`
- `__enter__()`
- `__exit__(type, value, traceback)`