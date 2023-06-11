# Use a custom verb

----

This stub shows how to implement a custom verb usage, here the client will send a "PING" request to the server, expecting a specific key in the response data : 

```
from anwdlclient.core.client import (
	ClientInterface, 
	REQUEST_VERB_STAT
)

SERVER_IP = "YOUR_SERVER_IP"

print(f"Connecting to {SERVER_IP} ...")
client = ClientInterface(server_ip=SERVER_IP)

print("Sending STAT request ...")
client.sendRequest("PING")
response = client.recvResponse()

if response[1]["success"]:
	print("Response from server : {}\n".format(
		response[1]["data"].get("answer"),
	))

else:
	print("An error occured : {}\n".format(response[1]["message"]))

client.closeConnection()
```