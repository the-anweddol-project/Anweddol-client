# Use a custom verb

----

This stub shows how to implement a custom verb usage, here the client will send a "PING" request to the server, expecting a specific key in the response data : 

```{warning}
This stub must be used with a server that handles the `"PING"` verb. Otherwise it will result as an unhandled verb error.
```

```
from anwdlclient.core.client import (
	ClientInterface, 
	REQUEST_VERB_STAT
)

SERVER_IP = "YOUR_SERVER_IP"

print(f"Connecting to {SERVER_IP} ...")
with ClientInterface(server_ip=SERVER_IP) as client:
	print("Sending STAT request ...")
	client.sendRequest("PING")

	is_response_valid, response_content, response_errors = client.recvResponse()

	if is_response_valid:
		print(
			f"Response from server : {response_content['data'].get('answer')}."
		)

	else:
		print(f"Received invalid response : {response_errors}\n")

```