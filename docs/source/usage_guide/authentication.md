# Authentication
---

The Anweddol server implementation uses a token system for authentication.

A token is a url-safe 124 characters long used on the implementation to restrict access.
These tokens are stored in a SQLite database file on the system, hashed with SHA256 for security reasons.

**NOTE** : There is only one token for one client, since a client cannot store 2 tokens for one same server.

## List recorded tokens

To list recorded tokens, execute :

```
$ anwdlclient token -l
```

It will list every entries with their ID, creation date and affiliated server IP.

## Add / delete a token

To add a token on local storage, execute : 

```
$ anwdlclient token -a <server_ip>
```

Then you'll need to paste the token when prompted, and press enter.
The specified token will be automatically sent to the server when connecting to it.

To delete a token, you need its entry ID.
First list the recorded tokens : 

```
$ anwdlclient token -l
```

Retrieve the ID of the entry in question, then execute : 

```
$ anwdlclient token -r <entry_id>
```

