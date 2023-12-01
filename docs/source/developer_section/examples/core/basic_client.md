# Basic client

----

Here is a basic client that you can use to send a STAT request to a server :

```
from anwdlclient.core.client import (
	ClientInterface, 
	REQUEST_VERB_STAT
)

SERVER_IP = "SERVER_IP"

with ClientInterface(SERVER_IP) as client:

	print(f"Connecting to {SERVER_IP} ...")
	client.connectServer()

	print("Sending STAT request ...")
	client.sendRequest(REQUEST_VERB_STAT)

	is_response_valid, response_content, response_errors = client.recvResponse()

	if is_response_valid:
		uptime = response_content["data"].get("uptime")

		print(f"The server is up, running since {uptime} seconds.")

	else:
		print(f"Received invalid response : {response_errors}")

```