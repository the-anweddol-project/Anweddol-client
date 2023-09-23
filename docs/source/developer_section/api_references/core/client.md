# Client

---

## class *ClientInterface*

### Definition

```{class} anwdlclient.core.client.ClientInterface(server_ip, server_listen_port, timeout, rsa_wrapper, aes_wrapper, auto_connect)
```

Represents a client to interact with servers.

```{tip}
This class can be used in a 'with' statement.
```

**Parameters** :

> ```{attribute} server_ip
> > Type : str
> 
> The server IP to connect to. Default is `None`.
> ```

> ```{attribute} server_port
> > Type : int
> 
> The remote server listen port. Default is `6150`.
> ```

> ```{attribute} timeout
> > Type : int
> 
> The timeout to set. Default is `None`.
> ```

> ```{attribute} rsa_wrapper
> > Type : `RSAWrapper`
> 
> The `RSAWrapper` instance that will be used on the client.
> ```

> ```{attribute} aes_wrapper
> > Type : `AESWrapper`
> 
> The `AESWrapper` instance that will be used on the client.
> ```

> ```{attribute} connect
> > Type : bool
> 
> `True` to connect to the specified server coordinates on initialization, `False` otherwise. Default is `True`.
> ```

```{note}
The connection is closed with the `closeConnection()` method when the `__del__` method is called.
```

```{warning}
If the parameter `connect` is set to `True` and no value is passed on the parameter `server_ip`, no connection will be made on initialization.
```

### Methods

```{classmethod} isClosed()
```

Check if the client socket is closed or not.

**Parameters** : 

> None

**Return value** :

> `True` if the client socket is closed, `False` otherwise.

---

```{classmethod} getSocketDescriptor()
```

Get the client socket descriptor

**Parameters** :

> None.

*Return value* :

> The socket descriptor of the client.

---

```{classmethod} getRSAWrapper()
```

Get the client `RSAWrapper` instance.

**Parameters** :

> None.

**Return value**:

> The `RSAWrapper` instance of the client.

---

```{classmethod} getAESWrapper()
```

Get the client `AESWrapper` instance.

**Parameters** :

> None.

**Return value**:

> The `AESWrapper` instance of the client.

---

```{classmethod} setRSAWrapper(rsa_wrapper)
```

Set the client `RSAWrapper` instance.

**Parameters** :

> ```{attribute} rsa_wrapper
> > Type : `RSAWrapper`
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
> > Type : `AESWrapper`
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
> > Type : bool
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
> > Type : str
> 
> The verb to send.
> ```

> ```{attribute} parameters
> > Type : dict
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

> The received response as a normalized [Response format](../../../technical_specifications/core/communication.md) dictionary.

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
