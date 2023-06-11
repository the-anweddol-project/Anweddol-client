# Developer section

----

Hello and welcome to the Anweddol client developer documentation.

Here, you'll find every informations and documentation about the client API features.

The Anweddol client is made with [python](https://www.python.org/).

**NOTE** : At the root of `anwdlclient`, there is the CLI source code : They are not meant to be used on an external program since it's the client implementation's code itself.

## Examples

See basic client stubs that can be used as examples.

```{toctree}
---
maxdepth: 3
includehidden:
---

examples/basic_client
```

```{toctree}
---
maxdepth: 3
includehidden:
---

examples/custom_verb_usage
```

## API references

Learn about every features that the `core` can provide.
You can see the *Technical specificatons* section to get every informations on how the Anweddol client works.

### Core features

The core features, also called `core`, are every needed functionnalities that an Anweddol client must have in order to correctly communicate with servers.

```{toctree}
---
maxdepth: 3
includehidden:
---

api_references/core/client
```

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

api_references/tools/accesstk
```

```{toctree}
---
maxdepth: 3
includehidden:
---

api_references/tools/credentials
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