# Basic client

----

Here is a basic client that you can use to send a STAT request to a server :

```
from anwdlclient.core.client import (
	ClientInterface, 
	REQUEST_VERB_STAT
)

SERVER_IP = "SERVER_IP"

print(f"Connecting to {SERVER_IP} ...")
client = ClientInterface(server_ip=SERVER_IP)

print("Sending STAT request ...")
client.sendRequest(REQUEST_VERB_STAT)
response = client.recvResponse()

if response[1]["success"]:
	print("The server is up, running since {} seconds with {} containers available.\n".format(
		response[1]["data"].get("uptime"),
		response[1]["data"].get("available"),
	))

else:
	print("An error occured : {}\n".format(response[1]["message"]))

client.closeConnection()
```