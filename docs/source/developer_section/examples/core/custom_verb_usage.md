# Use a custom verb

----

This stub shows how to implement a custom verb usage, here the client will send a "PING" request to the server, expecting a specific key in the response data : 

```{warning}
This stub must be used with the ["Handle a custom request verb" stub](https://anweddol-server.readthedocs.io/en/latest/developer_section/examples/core/custom_verb_handle.html) from the Anweddol server documentation, otherwise it will result as an unhandled verb error.
```

```
from anwdlclient.core.client import ClientInterface

SERVER_IP = "YOUR_SERVER_IP"

with ClientInterface(SERVER_IP) as client:

	print(f"Connecting to {SERVER_IP} ...")
	client.connectServer()

	print("Sending 'PING' request ...")
	client.sendRequest("PING")

	is_response_valid, response_content, response_errors = client.recvResponse()

	if is_response_valid:
		// Get the response key
		response = response_content['data'].get('response')

		print(f"Response from server : {response}.")

	else:
		print(f"Received invalid response : {response_errors}")

```