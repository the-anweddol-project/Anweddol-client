# Utilities
---

## System verification utilities

### Check if a port is bindable

```{function} anwdlclient.core.utilities.isPortBindable(port)
```

Check if a port is bindable.

**Parameters** :

> ```{attribute} port
> Type : int
> 
> The port whose bindability must be checked. It must be an integer between `1` and `65535`.
> ```

**Return value** : 

> Type : bool
>
> `True` if the port is bindable, `False` otherwise.

### Check if a socket is closed

```{function} anwdlclient.core.utilities.isSocketClosed(socket_descriptor)
```

Check if a socket descriptor is closed.

**Parameters** :

> ```{attribute} socket_descriptor
> Type : `socket.socket`
> 
> The socket descriptor to check.
> ```

**Return value** : 

> Type : bool
>
> `True` if the socket descriptor is closed, `False` otherwise.

## Format verification utilities

### Check if an IP is a valid IPv4 format

```{function} anwdlclient.core.utilities.isValidIP(ip)
```

Check if the IP is a valid IPv4 format.

**Parameters** :

> ```{attribute} ip
> Type : str
> 
> The IP to check as a string.
> ```

**Return value** : 

> Type : bool
>
> `True` if the IP is valid, `False` otherwise.
