# Developer section

----

Hello and welcome to the Anweddol client developer documentation.

Here, you'll find every informations and documentation about the [python](https://www.python.org/) client API features.

```{note}
At the root of `anwdlclient`, there is the CLI source code : They are not meant to be used on an external program.
```

## Examples

See basic client stubs that can be used as examples.

### `core` examples

```{toctree}
---
maxdepth: 3
includehidden:
---

examples/core/basic_client
```

```{toctree}
---
maxdepth: 3
includehidden:
---

examples/core/custom_verb_usage
```

### `web` examples

```{toctree}
---
maxdepth: 3
includehidden:
---

examples/web/basic_web_client
```

```{toctree}
---
maxdepth: 3
includehidden:
---

examples/web/basic_web_client_ssl
```

## API references

Learn about every features that the `core` can provide.

### Core features

The core features, also called `core`, are every needed functionnalities that an Anweddol client must have in order to correctly communicate with servers.

The `ClientInterface` class is the main client which encompasses all these features into a single and easy-to-use object : 

```{toctree}
---
maxdepth: 3
includehidden:
---

api_references/core/client
```

If you want to make a more complex use of Anweddol, you can retrieve every others `core` features documentations and references below : 

```{toctree}
---
maxdepth: 3
includehidden:
---

api_references/core/cryptography
```

```{toctree}
---
maxdepth: 3
includehidden:
---

api_references/core/sanitization
```

```{toctree}
---
maxdepth: 3
includehidden:
---

api_references/core/utilities
```

### Tools features

The `tools` features are additional functionnalities (access token, credentials, ...) coming with the Anweddol client package.

```{toctree}
---
maxdepth: 3
includehidden:
---

api_references/tools/access_token
```

```{toctree}
---
maxdepth: 3
includehidden:
---

api_references/tools/credentials
```

### Web features

The `web` features are additional functionnalities permitting HTTP interaction with Anweddol servers with the HTTP REST API available.

These are not essential features, although they can be used in specific contexts :

```{toctree}
---
maxdepth: 3
includehidden:
---

api_references/web/client
```

## CLI references

The actual Anweddol client CLI provides a JSON output feature that allows inter-program communication.

```{toctree}
---
maxdepth: 3
includehidden:
---

cli/json_output
```