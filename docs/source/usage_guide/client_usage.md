# Client usage
---

> You need to follows the [Installation](installation) section before continuing this tutorial.

Here is a typical tutorial on how to interact with a server, here 156.45.5.1.

## Send a STAT request to a server

If you want to create a container on a server, you first need to ensure if there is enough containers available before.

Send a STAT request by executing : 

```
$ anwdlclient stat 156.45.5.1
```

The server informations will be displayed.

## Send a CREATE request to a server

If there is enough containers left, you can send a CREATE request to the server : 

```
$ anwdlclient create 156.45.5.1
```

A container can take some time to create depending of the server's capacities, wait for the response.

When the response is received, grab the new created credentials entry ID and execute : 

```
$ anwdlclient container -p <entry_id>
```

to get the clear container SSH credentials to use.
Next, you can eventually establish a shell to it : 

```
$ ssh <container_username>@<container_ip> -p <container_listen_port>
```

Copy and paste the password, and you have now a shell on the container.

## Send a DESTROY request to a server

Once that the container fullfilled its initial task, we can destroy it on the server.

To do this, you need the credentials entry ID, then execute : 

```
$ anwdlclient destroy <entry_id>
```

The client will automatically fetch the server coordinates inside the specified entry, and send a DESTROY request to the server with the affiliated session credentials.

The specified entry will be deleted if the request is successful.