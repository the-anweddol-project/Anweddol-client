# Web client

---

## Constants

In the module `anwdlclient.web.client` : 

### Default values

Constant name                       | Value   | Definition
----------------------------------- | ------- | ----------
*DEFAULT_HTTP_SERVER_LISTEN_PORT*   | 8080    | The default HTTP web server listen port.
*DEFAULT_HTTPS_SERVER_LISTEN_PORT*  | 4443    | The default HTTPS web server listen port.
*DEFAULT_ENABLE_SSL*                | `False` | Enable SSL support by default or not.

## class *RESTWebServerInterface*

### Definition

```{class} anwdlclient.web.client.WebClientInterface(server_ip, server_listen_port, enable_ssl)
```

This class is the HTTP alternative to the classic `core` client. It gives the possibility to send HTTP requests on Anweddol servers HTTP REST API, if available.

The request / response scheme stays the same, except that they are exprimed in the form of an URL : "http(s)://server:port/verb". The server will respond by a JSON-formatted normalized [response dictionary](../../../technical_specifications/core/communication.md).

**Parameters** :

> ```{attribute} server_ip
> Type : str
> 
> The server IP to connect to. Must be an IPv4 format.
> ```

> ```{attribute} server_listen_port
> Type : int
> 
> The remote server listen port. Default is `8080`.
> ```

> ```{attribute} enable_ssl
> Type : bool
> 
> `True` to enable SSL support, `False` otherwise. Default is `False`.
> ```

```{warning}
If the parameter `enable_ssl` is set to `True`, you will probably need to change the remote server listen port. By convention the HTTPS port used by servers is the port `4443`, but any another one can be used : Make sure that the specified coordinates are correct.
```

### Request and reponse

```{classmethod} sendRequest(verb, parameters)
```

Send an HTTP request to the server.

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

> Type : tuple
>
> A tuple representing the return value of the `verifyResponseContent` function :
> 
> ```
> (
> 	is_response_format_valid,
> 	sanitized_response_dictionary,
> 	errors_dictionary,
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
> Raised in this method if the specified values are invalid.
> ```

> ```{exception} RuntimeError
> An error occured due to a failed internal action.
> 
> Raised in this method if the server returned a status code superior to 300. The actual received status code will be displayed in the exception message.
> ```

```{note}
Unlike the `core` client version under the same name, this method automatically handles the server response in its process.
```