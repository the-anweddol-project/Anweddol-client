# Credentials
---

Natively, there is 2 types of credentials : 

- The session credentials ;
- The container credentials ;

The Anweddol server CLI providing token authentication, a third one adds up : the authentication token credentials (see the [Access token](access_token) section to learn more).

## Session credentials

You can see the stored session credentials by executing :

```
$ anwdlclient session -l
```

This will print every session credentials database entries with their IDs, creation date and affiliated server IP. To get clear credentials of an entry, execute : 

```
$ anwdlclient session -p <entry_id>
```

To delete en entry, execute : 

```
$ anwdlclient session -d <entry id>
```

## Container credentials

You can see the stored container credentials by executing :

```
$ anwdlclient container -l
```

This will print every container credentials database entries with their IDs, creation date and affiliated server IP. To get clear credentials of an entry, execute : 

```
$ anwdlclient container -p <entry_id>
```

To delete en entry, execute : 

```
$ anwdlclient container -d <entry id>
```