# Web client

----

## Description

The `web` module is an HTTP alternative to the classic client. 

With it, you have the possibility to send HTTP requests on Anweddol servers
HTTP REST API, if provided.

## Request / response format

The request / response scheme stays the same, except that the requests are exprimed
in the form of an URL : "http://server:port/verb".

The server will respond by a JSON-formatted normalized [response dictionary](../core/communication.md).

## SSL support

The web server provides SSL support to allow secure communications between client and server.

```{warning}
Interactions with Anweddol servers HTTP REST API are possible with any kind of HTTP client, but note that if SSL is available on the server-side, there is a chance that the SSL certificate used by the server to encrypt communications is self-signed : It means that most modern HTTP clients will refuse the connection.

To avoid this, you should tell you HTTP client to ignore the error :

- With `curl` : Add the `--insecure` flag to the command.

  `$ curl https://<ip>:<port>/<verb> --insecure`

- With `wget` : Add the `--no-check-certificate` flag to the command.

  `$ wget https://<ip>:<port>/<verb> --no-check-certificate`

- With browsers : 

  Refer to the corresponding usage guide to ignore certificate errors.
```