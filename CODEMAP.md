# Code map

---

This file contains the source code files / folders mapping, with their respective descriptions.

> It is made for development guiding purposes.

## Source code tree

```
anwdlclient
├── cli.py
├── config.py
├── utilities.py
├── core
│   ├── client.py
│   ├── crypto.py
│   ├── sanitization.py
│   └── utilities.py
├── tools
│   ├── access_token.py
│   └── credentials.py
└── web
    └── client.py
```

### `anwdlclient` root files

- `cli.py` 

  This module contains the 'anwdlclient' CLI.

- `config.py` 

  This module provides the 'anwdlclient' CLI with configuration file management features.

- `utilities.py` 

  This module provides some miscellaneous features that the 'anwdlclient' CLI various modules uses in their processes.

### `anwdlserver` `core` folder content

- `client.py`

  This module is the main Anweddol client process.

  It connects every other core modules into a single one so that they can all be used in a single module.

- `crypto.py`

  This module provides the Anweddol client with RSA/AES encryption features.

  There is 2 provided encryption algorithms : RSA 4096 and AES 256 CBC.

- `sanitization.py`

  This module provides the Anweddol client with normalized request / response values and formats verification features.

- `utilities.py`

  This module contains miscellaneous features useful for the client.

### `anwdlserver` `tools` folder content

- `access_token.py`

  This module provides additional features for access token storage and management.

- `credentials.py`

  This module provides additional features for session and container credentials storage and management.

### `anwdlserver` `web` folder content

- `client.py`

  This module contains an HTTP alternative to the classic client. 

  With it, you have the possibility to send HTTP requests on Anweddol servers HTTP REST API, if provided.