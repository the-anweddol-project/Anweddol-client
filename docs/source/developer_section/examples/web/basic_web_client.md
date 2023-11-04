# Basic web client

----

Here is a simple web client stub that can be used to interact with an Anweddol server HTTP REST API :

```
from anwdlclient.web.client import (
	WebClientInterface,
	REQUEST_VERB_STAT
)

SERVER_IP = "SERVER_IP"

print(f"Connecting to {SERVER_IP} ...")

web_client = WebClientInterface(SERVER_IP)

print("Sending STAT request ...")
web_client.sendRequest(REQUEST_VERB_STAT)

is_response_valid, response_content, response_errors = web_client.recvResponse()

if is_response_valid:
	uptime = response_content["data"].get("uptime")

	print(f"The server is up, running since {uptime} seconds.")

else:
	print(f"Received invalid response : {response_errors}")

```