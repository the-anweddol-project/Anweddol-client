"""
Copyright 2023 The Anweddol project
See the LICENSE file for licensing informations
---

This module contains an HTTP alternative to the classic client. 
With it, you have the possibility to send HTTP requests on Anweddol servers
HTTP REST API, if provided.

The request / response scheme stays the same, except that they are exprimed
in the form of an URL : "http://<server:port>/<verb>".
The server responds by a JSON response containing a normalized response dictionary.

"""

import requests
import json

from ..core.sanitization import makeRequest, verifyResponseContent

# Default values
DEFAULT_HTTP_SERVER_LISTEN_PORT = 8080
DEFAULT_HTTPS_SERVER_LISTEN_PORT = 4443
DEFAULT_ENABLE_SSL = False


class WebClientInterface:
    def __init__(
        self,
        server_ip: str,
        server_listen_port: int = DEFAULT_HTTP_SERVER_LISTEN_PORT,
        enable_ssl: bool = DEFAULT_ENABLE_SSL,
    ):
        self.server_ip = server_ip
        self.enable_ssl = enable_ssl
        self.server_listen_port = server_listen_port

    def sendRequest(self, verb: str, parameters: dict = {}) -> None:
        is_request_valid, request_content, request_errors = makeRequest(
            verb, parameters=parameters
        )

        if not is_request_valid:
            raise ValueError(f"Error in specified values : {request_errors}")

        req = requests.post(
            f"http{'s' if self.enable_ssl else ''}://{self.server_ip}:{self.server_listen_port}/{verb.lower()}",
            data=json.dumps(request_content.get("parameters")),
            headers={"Content-Type": "application/json"},
        )

        if req.status_code >= 300:
            raise RuntimeError(f"Status code {req.status_code} from remote URL")

        return verifyResponseContent(req.json())
