# Access token

----

## class *AccessTokenManager*

### Definition

```{class} AccessTokenManager(access_token_db_path)
```

Provides access token storage and management functionnality.

```{tip}
This class can be used in a 'with' statement.
```

**Parameters** : 

> ```{attribute} access_token_db_path
> > Type : str
> 
> The access token database file path.
> ```

### General usage

```{classmethod} getDatabaseConnection()
```

Get the [`sqlite3.Connection`](https://docs.python.org/3.8/library/sqlite3.html#sqlite3.Connection) object of the instance.

**Parameters** : 

> None.

**Return value** : 

> The `sqlite3.Connection` object of the instance.

---

```{classmethod} getCursor()
```

Get the [`sqlite3.Cursor`](https://docs.python.org/3.8/library/sqlite3.html#sqlite3.Cursor) object of the instance.

**Parameters** : 

> None.

**Return value** : 

> The `sqlite3.Cursor` object of the instance.

---

```{classmethod} getEntryID(server_ip)
```

Get the entry ID of a specific IP.

**Parameters** : 

> ```{attribute} server_ip
> > Type : str
> 
> The server IP to search for.
> ```

**Return value** : 

> The entry ID of the specified IP if exists, `None` otherwise.

---

```{classmethod} getEntry(entry_id)
```

Get entry credentials.

**Parameters** : 

> ```{attribute} entry_id
> > Type : int
> 
> The entry ID to get the credentials from.
> ```

**Return value** : 

> A tuple representing the full entry row : 

> ```
> (
> 	entry_id,
> 	creation_timestamp,
> 	server_ip,
> 	server_port,
> 	access_token
> )
> ```

> - *entry_id* (Type : int)
> 
>   The entry ID.
> 
> - *creation_timestamp* (Type : int)
> 
>   The entry creation timestamp.
> 
> - *server_ip* (Type : str)
> 
>   The affiliated server IP.
> 
> - *server_port* (Type : int)
> 
>   The affiliated server port.
> 
> - *access_token* (Type : str)
> 
>   The access token, in plain text.

---

```{classmethod} addEntry(server_ip, server_port, access_token)
```

Add an entry.

**Parameters** : 

> ```{attribute} server_ip
> > Type : str
> 
> The server IP.
> ```

> ```{attribute} server_port
> > Type : int
> 
> The server listen port.
> ```

> ```{attribute} access_token
> > Type : str
> 
> The access token, in plain text.
> ```

**Return value** : 

> A tuple representing the infomations of the created entry :

> ```
> (
> 	entry_id,
> 	creation_timestamp
> )
> ```

- *entry_id* (Type : int)

  The new entry ID.

- *creation_timestamp* (Type : int)

  The entry ID creation timestamp.

```{warning}
Since the `access_token` value is meant to be read and reused later, it is stored in plain text on the database.
```

---

```{classmethod} listEntries()
```

List entries.

**Parameters** : 

> None.

**Return value** : 

> A list of tuples representing every session credentials entries on the database : 

> ```
> (
> 	entry_id,
> 	creation_timestamp,
> 	server_ip
> )
> ```

> - *entry_id* (Type : int)
> 
>   The new entry ID.
> 
> - *creation_timestamp* (Type : int)
> 
>   The entry creation timestamp.
> 
> - *server_ip* (Type : str)
> 
>   The affiliated server IP.

```{note}
Sensitive credentials arent listed with this method. Use the `getEntry` method to do so.
```

---

```{classmethod} deleteEntry(entry_id)
```

Delete an entry.

**Parameters** : 

> ```{attribute} entry_id
> > Type : int
> 
> The entry ID to delete on the database.
> ```

**Return value** : 

> `None`.

---

```{classmethod} closeDatabase()
```

Close the database.

**Parameters** :

> None.

**Return value** :

> `None`.

```{note} 
This method is automatically called within the `__del__` method.
```