# Sanitization

---

## Request and response formatting

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

> A tuple representing the verification results : 

> ```
> (
> 	True, 
> 	sanitized_response_dictionary
> )
> ```

> if the `response_dict` is a valid normalized [Response format](../../../technical_specifications/core/communication.md), 

> ```
> (
> 	False, 
> 	errors_dictionary
> )
> ```

> otherwise.

> - *sanitized_response_dictionary* (Type : dict)
> 
>   The sanitized response as a normalized [Response format](../../../technical_specifications/core/communication.md) dictionary.
> 
> - *errors_dictionary* (Type : dict)
> 
>   A dictionary depicting the errors detected in `response_dict` according to the [Cerberus](https://docs.python-cerberus.org/en/stable/errors.html) error format.

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

> A tuple representing a valid [Request format](../../../technical_specifications/core/communication.md) dictionary : 

> ```
> (
> 	True, 
> 	request_dictionary
> )
> ```

> if the operation succeeded, 

> ```
> (
> 	False,
> 	errors_dictionary
> )
> ```

> otherwise.

> - *request_dictionary* (Type : dict)
> 
>   The request dictionary as a normalized [Response format](../../../technical_specifications/core/communication.md).
> 
> - *errors_dictionary* (Type : dict)
> 
>   A dictionary depicting the errors detected in parameters according to the [Cerberus](https://docs.python-cerberus.org/en/stable/errors.html) error format.

```{note} 
The `sendRequest` method from `ClientInterface` wraps this function in its process. 
```

```{warning}
Like `verifyResponseContent`, the method only checks if the required keys and values exist and are correct, but it is open to unknown keys or structures for the developer to be able to implement its own mechanisms.
```
