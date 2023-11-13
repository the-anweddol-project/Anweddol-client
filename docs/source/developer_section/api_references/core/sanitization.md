# Sanitization

---

## Request and response format

### Verify a response content

```{function} anwdlclient.core.sanitize.verifyResponseContent(response_dict)
```

Check if a response dictionary is a valid normalized [Response format](../../../technical_specifications/core/communication.md).

**Parameters** :

> ```{attribute} response_dict
> > Type : dict
> 
> The response dictionary to verify.
> ```

**Return value** :

> Type : tuple
>
> A tuple representing the verification results :
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
>	Type : dict | `NoneType`
> 
>   The sanitized response as a normalized [Response format](../../../technical_specifications/core/communication.md) dictionary. `None` if `is_request_format_valid` is set to `False`.
> 
> - *errors_dictionary*
>
>	Type : dict | `NoneType`
> 
>   A dictionary depicting the errors detected in `response_dict` according to the [Cerberus](https://docs.python-cerberus.org/en/stable/errors.html) error format. `None` if `is_response_format_valid` is set to `True`.

```{warning} 
The method `verifyResponseContent` does not use strict verification. It only checks if the required keys and values exist and are correct, but it is open to unknown keys or structures for the developer to be able to implement its own mechanisms (See the technical specifications [Sanitization section](../../../technical_specifications/core/communication.md) to learn more).
```

### Make a normalized request

```{function} anwdlclient.core.sanitize.makeRequest(verb, parameters)
```

Make a normalized [Request format](../../../technical_specifications/core/communication.md) dictionary.

**Parameters** :

> ```{attribute} verb
> > Type : str
> 
> The verb to send.
> ```

> ```{attribute} parameters
> > Type : dict
> 
> The parameters to send. The content must be an empty dict or a normalized [Request format](../../../technical_specifications/core/communication.md).
> ```

**Return value** : 

> Type : tuple
>
> A tuple representing the verification results :

> ```
> (
> 	is_request_format_valid,
> 	sanitized_request_dictionary,
>   errors_dictionary,
> )
> ```

> - *is_request_format_valid*
>
>	Type : bool
> 
>   `True` if the request dictionary format is valid, `False` otherwise.
>
> - *sanitized_request_dictionary*
>
>	Type : dict | `NoneType`
> 
>   The sanitized request as a normalized [Request format](../../../technical_specifications/core/communication.md) dictionary. `None` if `is_request_format_valid` is set to `False`.
> 
> - *errors_dictionary*
>
>	Type : dict | `NoneType`
> 
>   A dictionary depicting the errors detected in `request_dict` according to the [Cerberus](https://docs.python-cerberus.org/en/stable/errors.html) error format. `None` if `is_request_format_valid` is set to `True`.

```{note} 
The `sendRequest` method from `ClientInterface` wraps this function in its process. 
```

```{warning}
Like `verifyResponseContent`, the method only checks if the required keys and values exist and are correct, but it is open to unknown keys or structures for the developer to be able to implement its own mechanisms.
```
