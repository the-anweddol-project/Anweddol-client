# Access token

----

The Anweddol server implementation can restrict its utilization by using the `tools` [Access token feature](../technical_specifications/tools/access_token.html) for client authentication.

An access token is a url-safe 124 characters long used on the implementation to restrict access.
These tokens are stored in a SQLite database file on the system.

```{note}
There is only one token for one client, since a client cannot store 2 tokens for one same server.
```

## List recorded tokens

To list recorded tokens, execute :

```
$ anwdlclient access-tk -l
```

It will list every entries with their ID, creation date and affiliated server IP.

## Add / delete a token

To add a token on local storage, execute : 

```
$ anwdlclient access-tk -a <server_ip>
```

Then you'll need to paste the token when prompted, and press enter.
The specified token will be automatically sent to the server when connecting to it.

To delete a token, you need its entry ID.
First list the recorded tokens : 

```
$ anwdlclient access-tk -l
```

Retrieve the ID of the entry in question, then execute : 

```
$ anwdlclient access-tk -d <entry_id>
```

