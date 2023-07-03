# Troubleshooting
---

Here is a list of non-exhaustive potential problems that can be encountered while using the Anweddol server : 


## `Failed to ... (reason : Internal error)`

It means that the remote server is experiencing an internal problem that makes it unavailable for the corresponding request.

Try again later, and if the problem persists you may contact the server administrator and report it.

## The client takes a long time connecting to servers

By default, the client will generate a new RSA key pair before connecting to the server.
This is because of privacy reasons : You are likely to be exposed to less tracking by randomizing your cryptographic fingerprint each time you use the client.

You can turn this off by modifying the `enable_onetime_rsa_keys` field of configuration file and set it to `False`, then the RSA keys stored in : 

- `~/.anweddol/rsa_keys` on linux ; 
- `C:\\Users\%USERNAME%\Anweddol\rsa_keys` on windows ;

will be used for each connection rather than being regenerated. 

**Be aware that doing this may lead to client recognition/tracking on the server side, and therefore infringe on your privacy.**