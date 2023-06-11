# Sanitization

---

> Normalized request / response values and formats

> Package `anwdlclient.core.sanitize`

## Constants

None

## Functions

```
verifyResponseContent(response_dict: dict) -> tuple
```

> Check if a response dictionary is a valid normalized [Response format](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#response-format)

_Parameters_ :

- `response_dict` : The response dictionary

_Return value_ :

- A tuple representing the verification results : 

```
(
	True, 
	sanitized_response_dictionary
)
```

if the `response_dict` is a valid normalized [Response format](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#response-format), 

```
(
	False, 
	errors_dictionary
)
```

otherwise.

- `sanitized_response_dictionary` : The sanitized response as a normalized [Response format](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#response-format) dictionary.
- `errors_dictionary` : A dictionary depicting the errors detected in `response_dict` according to the [Cerberus](https://docs.python-cerberus.org/en/stable/errors.html) error format.

**NOTE** : The method `verifyResponseContent` does not use strict verification. It only checks if the required keys and values exist and are correct, but it is open to unknown keys or structures for the developer to be able to implement its own mechanisms (See the technical specifications [Sanitization section](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#sanitization) to learn more).

---

```
makeRequest(verb: str, parameters: dict = {}) -> tuple:
```

> Make a normalized [Request format](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#request-format) dictionary

_Parameters_ :

- `verb` : The verb to send
- `parameters` : The parameters to send. The content must be an empty dict or a normalized [Request format](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#request-format).

_Return value_ : 

- A tuple representing a valid [Request format](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#request-format) dictionary : 

```
(
	True, 
	request_dictionary
)
```

if the operation succeeded, 

```
(
	False,
	errors_dictionary
)
```

otherwise.

- `request_dictionary` : The request dictionary as a normalized [Request format](https://anweddol-client.readthedocs.io/en/latest/technical_specifications/core/communication.html#request-format).
- `errors_dictionary` : A dictionary depicting the errors detected in parameters according to the [Cerberus](https://docs.python-cerberus.org/en/stable/errors.html) error format.

**NOTE** : The `sendRequest` method from `ClientInterface` wraps this function in its process. Like `verifyResponseContent`, the method only checks if the required keys and values exist and are correct, but it is open to unknown keys or structures for the developer to be able to implement its own mechanisms.
