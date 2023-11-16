# Client usage

---

```{warning}
You need to follows the [Installation](installation) section before continuing this tutorial.
```

Here is a typical tutorial on how to interact with an Anweddol server.

```{tip}
For each commands below, you can add the `-w` argument to interact with Anweddol servers HTTP REST API, if available.

If you want to use SSL, you should see the last section of this document about self-signed certificates.
```

## Send a STAT request to a server

If you want to create a container on a server, you first need to ensure if there is enough containers available before.

Send a STAT request by executing : 

```
$ anwdlclient stat <server_ip>
```

The server informations will be displayed.

## Send a CREATE request to a server

If there is enough containers left, you can send a CREATE request to the server : 

```
$ anwdlclient create <server_ip>
```

A container can take some time to create depending of the server's capacities, wait for the response.

When the response is received, grab the new created credentials entry ID and execute : 

```
$ anwdlclient container -p <entry_id>
```

to get the clear container SSH credentials to use. Next, you can establish a shell to it : 

```
$ ssh <container_username>@<server_ip> -p <container_listen_port>
```

Copy and paste the password, and you have now an SSH shell on the container.

## Send a DESTROY request to a server

Once that the container fullfilled its initial task, we can destroy it on the server.

To do this, you need the credentials entry ID, then execute : 

```
$ anwdlclient destroy <entry_id>
```

The client will automatically fetch the server coordinates inside the specified entry, and send a DESTROY request to the server with the affiliated session credentials.

The specified entry will be deleted if the request is successful.

```{note}
You can also shutdown the container domain from inside via SSH, the server will automatically destroy the container once detected as shutdown.
```

## Using server REST API with self-signed certificate

Interactions with Anweddol servers HTTP REST API are possible with any kind of HTTP client, but note that if SSL is available on the server-side, there is a chance that the SSL certificate used by the server to encrypt communications is self-signed : It means that most modern HTTP clients will refuse the connection.

To avoid this, you should tell you HTTP client to ignore the error :

- With `curl` : Add the `--insecure` flag to the command.

  `$ curl https://<ip>:<port>/<verb> --insecure`

- With `wget` : Add the `--no-check-certificate` flag to the command.

  `$ wget https://<ip>:<port>/<verb> --no-check-certificate`

- With browsers : 

  Refer to the corresponding usage guide to ignore certificate errors.

If you are using the `anwdlclient` CLI, you can simply add the `--no-ssl-verification` flag to the command to ignore SSL certificate verification.