# Credentials
---

Natively, there is 2 types of credentials : 
- The session credentials ;
- The container SSH credentials ;

The Anweddol server CLI providing token authentication, a third one adds up : the authentication token credentials (see the [Access token](access_token) section to learn more).

## Listing credentials entries

You can see the stored credentials by executing :

```
$ anwdlclient cred -l
```

This will print every credentials database entries with their IDs, creation date and affiliated server IP. To get clear credentials of an entry, execute : 

```
$ anwdlclient cred -p <entry_id>
```

## Delete an entry

To delete en entry, execute : 

```
$ anwdlclient cred -d <entry id>
```