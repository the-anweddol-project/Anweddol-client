"""
Copyright 2023 The Anweddol project
See the LICENSE file for licensing informations
---

This module contains the 'anwdlclient' executable CLI process.

"""

from datetime import datetime
from getpass import getpass
import argparse
import hashlib
import json
import sys
import os

# Intern importation
from .core.crypto import RSAWrapper, DEFAULT_RSA_KEY_SIZE
from .core.utilities import isValidIP
from .core.client import (
    ClientInterface,
    DEFAULT_SERVER_LISTEN_PORT,
    REQUEST_VERB_CREATE,
    REQUEST_VERB_DESTROY,
    REQUEST_VERB_STAT,
)
from .web.client import (
    WebClientInterface,
    DEFAULT_HTTP_SERVER_LISTEN_PORT,
    DEFAULT_ENABLE_SSL,
)
from .tools.credentials import SessionCredentialsManager, ContainerCredentialsManager
from .tools.access_token import AccessTokenManager

from .utilities import createFileRecursively, Colors
from .config import ConfigurationFileManager
from .__init__ import __version__


# Constants definition
PUBLIC_PEM_KEY_FILENAME = "public_key.pem"
PRIVATE_PEM_KEY_FILENAME = "private_key.pem"
CONFIG_FILE_PATH = (
    f"C:\\Users\\{os.getlogin()}\\Anweddol\\config.yaml"
    if os.name == "nt"
    else f"/home/{os.getlogin()}/.anweddol/config.yaml"
)

LOG_JSON_STATUS_SUCCESS = "OK"
LOG_JSON_STATUS_ERROR = "ERROR"

ERROR_INVALID_IP = -1
ERROR_INVALID_PORT = -2


class MainAnweddolClientCLI:
    def __init__(self):
        self.json = False

        try:
            if not os.path.exists(CONFIG_FILE_PATH):
                self._log_stdout(
                    f"The configuration file {CONFIG_FILE_PATH} was not found on system",
                    error=True,
                    color=Colors.RED,
                )

                exit(-1)

            self.config_manager = ConfigurationFileManager(CONFIG_FILE_PATH)
            (
                is_config_content_valid,
                config_validation_content,
            ) = self.config_manager.loadContent()

            if not is_config_content_valid:
                self._log_stdout(
                    "Error in configuration file :", error=True, color=Colors.RED
                )
                self._log_stdout(
                    json.dumps(config_validation_content, indent=4), error=True
                )

                exit(-1)

            self.config_content = config_validation_content

        except Exception as E:
            self._log_stdout(
                "An error occured during configuration file processing :",
                error=True,
                color=Colors.RED,
            )
            self._log_stdout(str(E), error=True)

            exit(-1)

        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage=f"""{sys.argv[0]} <command> [OPT] 

| The Anweddol client CLI implementation.
|
| Version {__version__}

server interaction commands:
  create      create a container on a remote server
  destroy     destroy a created container on a remote server
  stat        get runtime statistics of a remote server

credentials and authentication management commands:
  session     manage stored session credentials
  container   manage stored container credentials
  access-tk   manage access tokens
  regen-rsa   regenerate RSA keys""",
            epilog="""---
If you encounter any problems while using this tool,
please report it by opening an issue on the repository : 
 -> https://github.com/the-anweddol-project/Anweddol-client/issues""",
        )

        parser.add_argument("command", help="subcommand to run")
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command.replace("-", "_")):
            parser.print_help()
            exit(-1)

        try:
            exit(getattr(self, args.command.replace("-", "_"))())

        except Exception as E:
            if type(E) is KeyboardInterrupt:
                exit(0)

            if self.json:
                self._log_json(
                    LOG_JSON_STATUS_ERROR, "An error occured", result={"error": str(E)}
                )

            else:
                self._log_stdout("An error occured", color=Colors.RED, error=True)
                self._log_stdout(f"  Error : {E}", error=True)

            exit(-1)

    def _load_rsa_keys(self):
        self.runtime_rsa_wrapper = None

        if self.config_content.get("enable_onetime_rsa_keys"):
            return

        public_rsa_key_file_path = self.config_content.get("public_rsa_key_file_path")
        private_rsa_key_file_path = self.config_content.get("private_rsa_key_file_path")

        if not os.path.exists(private_rsa_key_file_path):
            createFileRecursively(private_rsa_key_file_path)

            self.runtime_rsa_wrapper = RSAWrapper()

            with open(public_rsa_key_file_path, "w") as fd:
                fd.write(self.runtime_rsa_wrapper.getPublicKey().decode())

            with open(private_rsa_key_file_path, "w") as fd:
                fd.write(self.runtime_rsa_wrapper.getPrivateKey().decode())

        else:
            self.runtime_rsa_wrapper = RSAWrapper(generate_key_pair=False)

            with open(private_rsa_key_file_path, "r") as fd:
                self.runtime_rsa_wrapper.setPrivateKey(
                    fd.read().encode(),
                    derivate_public_key=not os.path.exists(public_rsa_key_file_path),
                )

            if not os.path.exists(public_rsa_key_file_path):
                with open(public_rsa_key_file_path, "w") as fd:
                    fd.write(self.runtime_rsa_wrapper.getPublicKey().decode())

            else:
                with open(public_rsa_key_file_path, "r") as fd:
                    self.runtime_rsa_wrapper.setPublicKey(fd.read().encode())

    def _log_stdout(self, message, bypass=False, color=None, end="\n", error=False):
        if bypass:
            return

        print(
            f"{color}{message}\033[0;0m" if color else message,
            end=end,
            file=sys.stderr if error else sys.stdout,
        )

    def _log_json(self, status, message, result={}):
        print(json.dumps({"status": status, "message": message, "result": result}))

    def _check_parameters_validity(self, ip=None, port=None):
        if ip and not isValidIP(ip):
            return ERROR_INVALID_IP

        if port and (port >= 65535 or port <= 0):
            return ERROR_INVALID_PORT

    def create(self):
        parser = argparse.ArgumentParser(
            description="| Create a container on a remote server",
            usage=f"""{sys.argv[0]} create <IP> [OPT]""",
        )
        parser.add_argument("ip", help="specify the server IP", type=str)
        parser.add_argument(
            "-p", "--port", help="specify the server listen port", type=int
        )
        parser.add_argument(
            "-w", "--web", help="use the web version of the client", action="store_true"
        )
        parser.add_argument(
            "-s",
            "--ssl",
            help="enable SSL for HTTP communications",
            action="store_true",
        )
        parser.add_argument(
            "--no-ssl-verification",
            help="do not verify the server SSL certificate (for self-signed ones)",
            action="store_true",
        )
        parser.add_argument(
            "--show-credentials",
            help="display the received credentials in the terminal",
            action="store_true",
        )
        parser.add_argument(
            "--do-not-store",
            help="do not store received credentials",
            action="store_true",
        )
        parser.add_argument(
            "--json", help="print output in JSON format", action="store_true"
        )
        args = parser.parse_args(sys.argv[2:])

        self.json = args.json
        self._load_rsa_keys()

        check_result = self._check_parameters_validity(args.ip, args.port)
        if check_result == ERROR_INVALID_IP:
            if args.json:
                self._log_json(
                    LOG_JSON_STATUS_ERROR,
                    f"'{args.ip}' is not a valid IPv4 IP format",
                )

            else:
                self._log_stdout(
                    f"'{args.ip}' is not a valid IPv4 IP format",
                    color=Colors.RED,
                    error=True,
                )

            return -1

        if check_result == ERROR_INVALID_PORT:
            if args.json:
                self._log_json(
                    LOG_JSON_STATUS_ERROR,
                    f"'{args.port}' is not a non-zero integer less than 65535",
                )

            else:
                self._log_stdout(
                    f"'{args.port}' is not a non-zero integer less than 65535",
                    color=Colors.RED,
                    error=True,
                )

            return -1

        access_token_db_file_path = self.config_content.get("access_token_db_file_path")
        session_credentials_db_file_path = self.config_content.get(
            "session_credentials_db_file_path"
        )
        container_credentials_db_file_path = self.config_content.get(
            "container_credentials_db_file_path"
        )

        if not os.path.exists(access_token_db_file_path):
            createFileRecursively(access_token_db_file_path)

        if not os.path.exists(session_credentials_db_file_path):
            createFileRecursively(session_credentials_db_file_path)

        if not os.path.exists(container_credentials_db_file_path):
            createFileRecursively(container_credentials_db_file_path)

        request_parameters = {}

        with AccessTokenManager(access_token_db_file_path) as access_token_manager:
            entry_id = access_token_manager.getEntryID(args.ip)

            if entry_id:
                request_parameters.update(
                    {"access_token": access_token_manager.getEntry(entry_id)[4]}
                )

        if args.web:
            web_client = WebClientInterface(
                args.ip,
                server_listen_port=args.port
                if args.port
                else DEFAULT_HTTP_SERVER_LISTEN_PORT,
                enable_ssl=args.ssl if args.ssl else DEFAULT_ENABLE_SSL,
            )

            self._log_stdout(
                "Sending request, waiting for response. This can take some time ... ",
                bypass=args.json,
            )

            (
                is_response_valid,
                response_content,
                response_error_dict,
            ) = web_client.sendRequest(
                REQUEST_VERB_CREATE,
                parameters=request_parameters,
                verify_ssl_certificate=not args.no_ssl_verification,
            )

        else:
            with ClientInterface(
                args.ip,
                server_listen_port=args.port
                if args.port
                else DEFAULT_SERVER_LISTEN_PORT,
                rsa_wrapper=self.runtime_rsa_wrapper,
            ) as client:
                client.connectServer()
                client.sendRequest(
                    REQUEST_VERB_CREATE,
                    parameters=request_parameters,
                )

                self._log_stdout(
                    "Request sent, waiting for response. This can take some time ... ",
                    bypass=args.json,
                )

                (
                    is_response_valid,
                    response_content,
                    response_error_dict,
                ) = client.recvResponse()

        if not is_response_valid:
            if args.json:
                self._log_json(
                    LOG_JSON_STATUS_ERROR,
                    "Received invalid response",
                    result={"error_dict": response_error_dict},
                )

            else:
                self._log_stdout(
                    "Received invalid response", color=Colors.RED, error=True
                )
                self._log_stdout(
                    f"  Error(s) : {json.dumps(response_error_dict, indent=4)}",
                    error=True,
                )

            return -1

        message = response_content.get("message")

        if not response_content["success"]:
            if args.json:
                self._log_json(
                    LOG_JSON_STATUS_ERROR,
                    "Failed to create container",
                    result={"response": response_content},
                )

            else:
                self._log_stdout(
                    "Failed to create container", color=Colors.RED, error=True
                )
                self._log_stdout(f"  Message : {message}", error=True)

            return -1

        container_iso_sha256 = response_content["data"].get("container_iso_sha256")
        container_uuid = response_content["data"].get("container_uuid")
        client_token = response_content["data"].get("client_token")
        container_username = response_content["data"].get("container_username")
        container_password = response_content["data"].get("container_password")
        container_listen_port = response_content["data"].get("container_listen_port")

        self._log_stdout(
            "Container successfully created", bypass=args.json, color=Colors.GREEN
        )
        self._log_stdout(f"  Message : {message}", bypass=args.json)
        self._log_stdout(
            f"  Container ISO checksum : {container_iso_sha256}", bypass=args.json
        )

        if args.show_credentials and not args.json:
            self._log_stdout("Session credentials :")
            self._log_stdout(f"  Container UUID : {container_uuid}")
            self._log_stdout(f"  Client token : {client_token}")
            self._log_stdout(f"  Container username : {container_username}")
            self._log_stdout(f"  Container password : {container_password}")
            self._log_stdout(f"  Container listen port : {container_listen_port}")

        if not args.do_not_store:
            with SessionCredentialsManager(
                session_credentials_db_file_path
            ) as session_credentials_manager:
                (
                    new_session_credentials_entry_id,
                    _,
                ) = session_credentials_manager.addEntry(
                    args.ip,
                    args.port
                    if args.port
                    else (
                        DEFAULT_SERVER_LISTEN_PORT
                        if not args.web
                        else DEFAULT_HTTP_SERVER_LISTEN_PORT
                    ),
                    container_uuid,
                    client_token,
                )

                self._log_stdout(
                    f"  Session credentials ID : {new_session_credentials_entry_id}",
                    bypass=args.json,
                )

            with ContainerCredentialsManager(
                container_credentials_db_file_path
            ) as container_credentials_manager:
                (
                    new_container_credentials_entry_id,
                    _,
                ) = container_credentials_manager.addEntry(
                    args.ip,
                    args.port
                    if args.port
                    else (
                        DEFAULT_SERVER_LISTEN_PORT
                        if not args.web
                        else DEFAULT_HTTP_SERVER_LISTEN_PORT
                    ),
                    container_username,
                    container_password,
                    container_listen_port,
                )

                self._log_stdout(
                    f"  Container credentials ID : {new_container_credentials_entry_id}",
                    bypass=args.json,
                )

        if args.json:
            self._log_json(
                LOG_JSON_STATUS_SUCCESS,
                "Container successfully created",
                result={
                    "message": message,
                    "data": response_content.get("data"),
                    "session_entry_id": new_session_credentials_entry_id,
                    "container_entry_id": new_container_credentials_entry_id,
                },
            )

        return 0

    def destroy(self):
        parser = argparse.ArgumentParser(
            description="| Destroy a created container on a remote server",
            usage=f"{sys.argv[0]} destroy <session_entry_id> [OPT] ",
        )
        parser.add_argument(
            "session_entry_id", help="specify the local session ID", type=int
        )
        parser.add_argument(
            "-w", "--web", help="use the web version of the client", action="store_true"
        )
        parser.add_argument(
            "-s",
            "--ssl",
            help="enable SSL for HTTP communications",
            action="store_true",
        )
        parser.add_argument(
            "--no-ssl-verification",
            help="do not verify the server SSL certificate (for self-signed ones)",
            action="store_true",
        )
        parser.add_argument(
            "--do-not-delete",
            help="do not delete credentials on local storage",
            action="store_true",
        )
        parser.add_argument(
            "--json", help="print output in JSON format", action="store_true"
        )
        args = parser.parse_args(sys.argv[2:])

        self.json = args.json
        self._load_rsa_keys()

        access_token_db_file_path = self.config_content.get("access_token_db_file_path")
        session_credentials_db_file_path = self.config_content.get(
            "session_credentials_db_file_path"
        )
        container_credentials_db_file_path = self.config_content.get(
            "container_credentials_db_file_path"
        )

        if not os.path.exists(access_token_db_file_path):
            createFileRecursively(access_token_db_file_path)

        if not os.path.exists(session_credentials_db_file_path):
            createFileRecursively(session_credentials_db_file_path)

        if not os.path.exists(container_credentials_db_file_path):
            createFileRecursively(container_credentials_db_file_path)

        session_credentials_manager = SessionCredentialsManager(
            session_credentials_db_file_path
        )
        entry_content = session_credentials_manager.getEntry(args.session_entry_id)

        if not entry_content:
            if args.json:
                self._log_json(
                    LOG_JSON_STATUS_ERROR,
                    f"Session ID '{args.session_entry_id}' does not exists",
                )

            else:
                self._log_stdout(
                    f"Session ID '{args.session_entry_id}' does not exists",
                    color=Colors.RED,
                    error=True,
                )

            return -1

        (
            entry_id,
            _,
            server_ip,
            server_port,
            container_uuid,
            client_token,
        ) = entry_content

        request_parameters = {
            "container_uuid": container_uuid,
            "client_token": client_token,
        }

        with AccessTokenManager(access_token_db_file_path) as access_token_manager:
            entry_id = access_token_manager.getEntryID(server_ip)

            if entry_id:
                request_parameters.update(
                    {"access_token": access_token_manager.getEntry(entry_id)[4]}
                )

        try:
            if args.web:
                client = WebClientInterface(
                    server_ip,
                    server_listen_port=server_port,
                    enable_ssl=args.ssl if args.ssl else DEFAULT_ENABLE_SSL,
                )

                (
                    is_response_valid,
                    response_content,
                    response_error_dict,
                ) = client.sendRequest(
                    REQUEST_VERB_DESTROY,
                    parameters=request_parameters,
                    verify_ssl_certificate=not args.no_ssl_verification,
                )

            else:
                with ClientInterface(
                    server_ip,
                    server_listen_port=server_port,
                    rsa_wrapper=self.runtime_rsa_wrapper,
                ) as client:
                    client.connectServer()
                    client.sendRequest(
                        REQUEST_VERB_DESTROY,
                        parameters=request_parameters,
                    )

                    (
                        is_response_valid,
                        response_content,
                        response_error_dict,
                    ) = client.recvResponse()

            if not is_response_valid:
                if args.json:
                    self._log_json(
                        LOG_JSON_STATUS_ERROR,
                        "Received invalid response",
                        result={"error_dict": response_error_dict},
                    )

                else:
                    self._log_stdout(
                        "Received invalid response", color=Colors.RED, error=True
                    )
                    self._log_stdout(
                        f"  Error(s) : {json.dumps(response_error_dict, indent=4)}",
                        error=True,
                    )

                session_credentials_manager.closeDatabase()

                return -1

            message = response_content.get("message")

            if not response_content["success"]:
                if args.json:
                    self._log_json(
                        LOG_JSON_STATUS_ERROR,
                        "Failed to destroy container",
                        result={"response": response_content},
                    )

                else:
                    self._log_stdout(
                        "Failed to destroy container", color=Colors.RED, error=True
                    )
                    self._log_stdout(f"  Message : {message}", error=True)

                session_credentials_manager.closeDatabase()

                return -1

            if not args.do_not_delete:
                session_credentials_manager.deleteEntry(args.session_entry_id)

                with ContainerCredentialsManager(
                    container_credentials_db_file_path
                ) as container_credentials_manager:
                    container_entry_id = container_credentials_manager.getEntryID(
                        server_ip
                    )

                    if container_entry_id:
                        container_credentials_manager.deleteEntry(container_entry_id)

            if args.json:
                self._log_json(
                    LOG_JSON_STATUS_SUCCESS,
                    "Container successfully destroyed",
                    result={"message": message},
                )

            else:
                self._log_stdout("Container successfully destroyed", color=Colors.GREEN)
                self._log_stdout(f"  Message : {message}")

            session_credentials_manager.closeDatabase()

            return 0

        except Exception as E:
            session_credentials_manager.closeDatabase()
            raise E

    def stat(self):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="| Retrieve runtime statistics of a remote server",
            usage=f"{sys.argv[0]} stat <ip> [OPT] ",
        )

        parser.add_argument("ip", help="specify the server IP", type=str)
        parser.add_argument(
            "-p", "--port", help="specify the server listen port", type=int
        )
        parser.add_argument(
            "-w", "--web", help="use the web version of the client", action="store_true"
        )
        parser.add_argument(
            "-s",
            "--ssl",
            help="enable SSL for HTTP communications",
            action="store_true",
        )
        parser.add_argument(
            "--no-ssl-verification",
            help="do not verify the server SSL certificate (for self-signed ones)",
            action="store_true",
        )
        parser.add_argument(
            "--json", help="print output in JSON format", action="store_true"
        )
        args = parser.parse_args(sys.argv[2:])

        self.json = args.json

        check_result = self._check_parameters_validity(args.ip, args.port)
        if check_result == ERROR_INVALID_IP:
            if args.json:
                self._log_json(
                    LOG_JSON_STATUS_ERROR,
                    f"'{args.ip}' is not a valid IPv4 IP format",
                )

            else:
                self._log_stdout(
                    f"'{args.ip}' is not a valid IPv4 IP format",
                    color=Colors.RED,
                    error=True,
                )

            return -1

        if check_result == ERROR_INVALID_PORT:
            if args.json:
                self._log_json(
                    LOG_JSON_STATUS_ERROR,
                    f"'{args.port}' is not a non-zero integer less than 65535",
                )

            else:
                self._log_stdout(
                    f"'{args.port}' is not a non-zero integer less than 65535",
                    color=Colors.RED,
                    error=True,
                )

            return -1

        self._load_rsa_keys()
        access_token_db_file_path = self.config_content.get("access_token_db_file_path")

        if not os.path.exists(access_token_db_file_path):
            createFileRecursively(access_token_db_file_path)

        request_parameters = {}

        with AccessTokenManager(access_token_db_file_path) as access_token_manager:
            entry_id = access_token_manager.getEntryID(args.ip)

            if entry_id:
                request_parameters.update(
                    {"access_token": access_token_manager.getEntry(entry_id)[4]}
                )

        if args.web:
            client = WebClientInterface(
                args.ip,
                server_listen_port=args.port
                if args.port
                else DEFAULT_HTTP_SERVER_LISTEN_PORT,
                enable_ssl=args.ssl if args.ssl else DEFAULT_ENABLE_SSL,
            )

            (
                is_response_valid,
                response_content,
                response_error_dict,
            ) = client.sendRequest(
                REQUEST_VERB_STAT,
                parameters=request_parameters,
                verify_ssl_certificate=not args.no_ssl_verification,
            )

        else:
            with ClientInterface(
                args.ip,
                server_listen_port=args.port
                if args.port
                else DEFAULT_SERVER_LISTEN_PORT,
                rsa_wrapper=self.runtime_rsa_wrapper,
            ) as client:
                client.connectServer()
                client.sendRequest(
                    REQUEST_VERB_STAT,
                    parameters=request_parameters,
                )

                (
                    is_response_valid,
                    response_content,
                    response_error_dict,
                ) = client.recvResponse()

        if not is_response_valid:
            if args.json:
                self._log_json(
                    LOG_JSON_STATUS_ERROR,
                    "Received invalid response",
                    result={"error_dict": response_error_dict},
                )

            else:
                self._log_stdout(
                    "Received invalid response", color=Colors.RED, error=True
                )
                self._log_stdout(
                    f"  Error(s) : {json.dumps(response_error_dict, indent=4)}",
                    error=True,
                )

            return -1

        message = response_content.get("message")

        if not response_content["success"]:
            if args.json:
                self._log_json(
                    LOG_JSON_STATUS_ERROR,
                    "Failed to stat server",
                    result={"response": response_content},
                )

            else:
                self._log_stdout("Failed to stat server", color=Colors.RED, error=True)
                self._log_stdout(f"  Message : {message}", error=True)

            return -1

        version = response_content["data"].get("version")
        uptime = response_content["data"].get("uptime")
        available = response_content["data"].get("available")

        if args.json:
            self._log_json(
                LOG_JSON_STATUS_SUCCESS,
                "Server statistics",
                result={
                    "message": message,
                    "data": response_content.get("data"),
                },
            )

        else:
            self._log_stdout("Server statistics :")
            self._log_stdout(f"  Version : {version}")
            self._log_stdout(f"  Uptime : {uptime}")
            self._log_stdout(f"  Available containers : {available}")

        return 0

    def session(self):
        parser = argparse.ArgumentParser(
            description="| Manage stored session credentials",
            usage=f"{sys.argv[0]} session [OPT] ",
        )
        parser.add_argument(
            "-l", help="list recorded credentials entries", action="store_true"
        )
        parser.add_argument(
            "-p",
            help="get entry credentials",
            dest="get_entry",
            metavar="ENTRY_ID",
            type=int,
        )
        parser.add_argument(
            "-d",
            help="delete entry credentials",
            dest="delete_entry",
            metavar="ENTRY_ID",
            type=int,
        )
        parser.add_argument(
            "--json", help="print output in JSON format", action="store_true"
        )
        args = parser.parse_args(sys.argv[2:])

        self.json = args.json

        session_credentials_db_file_path = self.config_content.get(
            "session_credentials_db_file_path"
        )

        if not os.path.exists(session_credentials_db_file_path):
            createFileRecursively(session_credentials_db_file_path)

        with SessionCredentialsManager(
            session_credentials_db_file_path
        ) as session_credentials_manager:
            if args.l:
                if args.json:
                    self._log_json(
                        LOG_JSON_STATUS_SUCCESS,
                        "Recorded entries ID",
                        result={
                            "entry_list": session_credentials_manager.listEntries()
                        },
                    )

                else:
                    for (
                        entry_id,
                        creation_timestamp,
                        server_ip,
                    ) in session_credentials_manager.listEntries():
                        self._log_stdout(f"- Entry ID {entry_id}")
                        self._log_stdout(
                            f"  Created : {datetime.fromtimestamp(creation_timestamp)}"
                        )
                        self._log_stdout(f"  Server IP : {server_ip}\n")

            elif args.get_entry:
                credentials = session_credentials_manager.getEntry(args.get_entry)

                if not credentials:
                    if args.json:
                        self._log_json(
                            LOG_JSON_STATUS_ERROR,
                            f"Entry ID '{args.get_entry}' does not exists",
                        )

                    else:
                        self._log_stdout(
                            f"Entry ID '{args.get_entry}' does not exists",
                            color=Colors.RED,
                            error=True,
                        )

                    return -1

                (
                    _,
                    creation_timestamp,
                    server_ip,
                    server_port,
                    container_uuid,
                    client_token,
                ) = credentials

                if args.json:
                    self._log_json(
                        LOG_JSON_STATUS_SUCCESS,
                        "Entry ID content",
                        result={
                            "created": creation_timestamp,
                            "server_ip": server_ip,
                            "server_port": server_port,
                            "container_uuid": container_uuid,
                            "client_token": client_token,
                        },
                    )

                else:
                    self._log_stdout(f"Entry ID {args.get_entry} content :")
                    self._log_stdout(
                        f"  Created : {datetime.fromtimestamp(creation_timestamp)}"
                    )
                    self._log_stdout(f"  Server IP : {server_ip}")
                    self._log_stdout(f"  Server port : {server_port}")
                    self._log_stdout(f"  Container UUID : {container_uuid}")
                    self._log_stdout(f"  Client token : {client_token}")

            else:
                if not session_credentials_manager.getEntry(args.delete_entry):
                    if args.json:
                        self._log_json(
                            LOG_JSON_STATUS_ERROR,
                            f"Entry ID '{args.delete_entry}' does not exists",
                        )

                    else:
                        self._log_stdout(
                            f"Entry ID '{args.delete_entry}' does not exists",
                            color=Colors.RED,
                            error=True,
                        )

                    return -1

                session_credentials_manager.deleteEntry(args.delete_entry)

            return 0

    def container(self):
        parser = argparse.ArgumentParser(
            description="| Manage stored container credentials",
            usage=f"{sys.argv[0]} container [OPT] ",
        )
        parser.add_argument(
            "-l", help="list recorded credentials entries", action="store_true"
        )
        parser.add_argument(
            "-p",
            help="get entry credentials",
            dest="get_entry",
            metavar="ENTRY_ID",
            type=int,
        )
        parser.add_argument(
            "-d",
            help="delete entry credentials",
            dest="delete_entry",
            metavar="ENTRY_ID",
            type=int,
        )
        parser.add_argument(
            "--json", help="print output in JSON format", action="store_true"
        )
        args = parser.parse_args(sys.argv[2:])

        self.json = args.json

        container_credentials_db_file_path = self.config_content.get(
            "container_credentials_db_file_path"
        )

        if not os.path.exists(container_credentials_db_file_path):
            createFileRecursively(container_credentials_db_file_path)

        with ContainerCredentialsManager(
            container_credentials_db_file_path
        ) as container_credentials_manager:
            if args.l:
                if args.json:
                    self._log_json(
                        LOG_JSON_STATUS_SUCCESS,
                        "Recorded entries ID",
                        result={
                            "entry_list": container_credentials_manager.listEntries()
                        },
                    )

                else:
                    for (
                        entry_id,
                        creation_timestamp,
                        server_ip,
                    ) in container_credentials_manager.listEntries():
                        self._log_stdout(f"- Entry ID {entry_id}")
                        self._log_stdout(
                            f"  Created : {datetime.fromtimestamp(creation_timestamp)}"
                        )
                        self._log_stdout(f"  Server IP : {server_ip}\n")

            elif args.get_entry:
                credentials = container_credentials_manager.getEntry(args.get_entry)

                if not credentials:
                    container_credentials_manager.closeDatabase()
                    if args.json:
                        self._log_json(
                            LOG_JSON_STATUS_ERROR,
                            f"Entry ID '{args.get_entry}' does not exists",
                        )

                    else:
                        self._log_stdout(
                            f"Entry ID '{args.get_entry}' does not exists",
                            color=Colors.RED,
                            error=True,
                        )

                    return -1

                (
                    _,
                    creation_timestamp,
                    server_ip,
                    server_port,
                    container_username,
                    container_password,
                    container_listen_port,
                ) = credentials

                if args.json:
                    self._log_json(
                        LOG_JSON_STATUS_SUCCESS,
                        "Entry ID content",
                        result={
                            "created": creation_timestamp,
                            "server_ip": server_ip,
                            "server_port": server_port,
                            "container_username": container_username,
                            "container_password": container_password,
                            "container_listen_port": container_listen_port,
                        },
                    )

                else:
                    self._log_stdout(f"Entry ID {args.get_entry} content :")
                    self._log_stdout(
                        f"  Created : {datetime.fromtimestamp(creation_timestamp)}"
                    )
                    self._log_stdout(f"  Server IP : {server_ip}")
                    self._log_stdout(f"  Server port : {server_port}")
                    self._log_stdout(f"  SSH username : {container_username}")
                    self._log_stdout(f"  SSH password : {container_password}")
                    self._log_stdout(f"  SSH listen port : {container_listen_port}")

            else:
                if args.delete_entry:
                    if not container_credentials_manager.getEntry(args.delete_entry):
                        if args.json:
                            self._log_json(
                                LOG_JSON_STATUS_ERROR,
                                f"Entry ID '{args.delete_entry}' does not exists",
                            )

                        else:
                            self._log_stdout(
                                f"Entry ID '{args.delete_entry}' does not exists",
                                color=Colors.RED,
                                error=True,
                            )

                        return -1

                    container_credentials_manager.deleteEntry(args.delete_entry)

            return 0

    def access_tk(self):
        parser = argparse.ArgumentParser(
            description="| Manage access tokens",
            usage=f"{sys.argv[0]} access-tk [OPT] ",
            epilog="(*) Input pipe is needed if used with the --json flag : 'echo <token> | anwdlclient access-tk -a <server_ip> --json'",
        )
        parser.add_argument(
            "-l", help="list recorded tokens entries", action="store_true"
        )
        parser.add_argument(
            "-a",
            help="add a token entry (*)",
            dest="server_ip",
            type=str,
        )
        parser.add_argument(
            "-p",
            help="print a token entry",
            dest="print_entry",
            metavar="ENTRY_ID",
            type=int,
        )
        parser.add_argument(
            "-d",
            help="delete an entry",
            dest="delete_entry",
            metavar="ENTRY_ID",
            type=int,
        )
        parser.add_argument(
            "--port",
            help="specify the server listen port",
            dest="server_port",
            type=int,
        )
        parser.add_argument(
            "--json", help="print output in JSON format", action="store_true"
        )
        args = parser.parse_args(sys.argv[2:])

        self.json = args.json

        access_token_db_file_path = self.config_content.get("access_token_db_file_path")

        if not os.path.exists(access_token_db_file_path):
            createFileRecursively(access_token_db_file_path)

        with AccessTokenManager(access_token_db_file_path) as access_token_manager:
            if args.l:
                if args.json:
                    self._log_json(
                        LOG_JSON_STATUS_SUCCESS,
                        "Recorded entries ID",
                        result={"entry_list": access_token_manager.listEntries()},
                    )

                else:
                    for (
                        entry_id,
                        creation_timestamp,
                        server_ip,
                    ) in access_token_manager.listEntries():
                        self._log_stdout(f"- Entry ID {entry_id}")
                        self._log_stdout(
                            f"  Created : {datetime.fromtimestamp(creation_timestamp)}"
                        )
                        self._log_stdout(f"  Server IP : {server_ip}\n")

            elif args.server_ip:
                check_result = self._check_parameters_validity(args.server_ip)
                if check_result == ERROR_INVALID_IP:
                    if args.json:
                        self._log_json(
                            LOG_JSON_STATUS_ERROR,
                            f"'{args.server_ip}' is not a valid IPv4 IP format",
                        )

                    else:
                        self._log_stdout(
                            f"'{args.server_ip}' is not a valid IPv4 IP format",
                            color=Colors.RED,
                            error=True,
                        )

                    return -1

                if access_token_manager.getEntryID(args.server_ip):
                    if args.json:
                        self._log_json(
                            LOG_JSON_STATUS_ERROR,
                            f"'{args.server_ip}' is already specified on database",
                        )

                    else:
                        self._log_stdout(
                            f"'{args.server_ip}' is already specified on database",
                            color=Colors.RED,
                            error=True,
                        )

                    return -1

                new_access_token = (
                    getpass(prompt="Paste the new token : ")
                    if not args.json
                    else input("")
                )
                new_entry_id, _ = access_token_manager.addEntry(
                    args.server_ip,
                    args.server_port
                    if args.server_port
                    else DEFAULT_SERVER_LISTEN_PORT,
                    new_access_token,
                )

                if args.json:
                    self._log_json(
                        LOG_JSON_STATUS_SUCCESS,
                        "New token entry created",
                        result={"entry_id": new_entry_id},
                    )

                else:
                    self._log_stdout("New token entry created", color=Colors.GREEN)
                    self._log_stdout(f"  Entry ID : {new_entry_id}")

            elif args.print_entry:
                entry_content = access_token_manager.getEntry(args.print_entry)

                if not entry_content:
                    if args.json:
                        self._log_json(
                            LOG_JSON_STATUS_ERROR,
                            f"Entry ID '{args.print_entry}' does not exists",
                        )

                    else:
                        self._log_stdout(
                            f"Entry ID '{args.print_entry}' does not exists",
                            color=Colors.RED,
                            error=True,
                        )

                    return -1

                (
                    _,
                    creation_timestamp,
                    server_ip,
                    server_port,
                    access_token,
                ) = entry_content

                if args.json:
                    self._log_json(
                        LOG_JSON_STATUS_SUCCESS,
                        "Entry ID content",
                        result={
                            "created": creation_timestamp,
                            "server_ip": server_ip,
                            "server_port": server_port,
                            "access_token": access_token,
                        },
                    )

                else:
                    self._log_stdout(f"Entry ID {args.print_entry} content :")
                    self._log_stdout(
                        f"  Created : {datetime.fromtimestamp(creation_timestamp)}"
                    )
                    self._log_stdout(f"  Server IP : {server_ip}")
                    self._log_stdout(f"  Server port : {server_port}")
                    self._log_stdout(f"  Access token : {access_token}")

            else:
                if not access_token_manager.getEntry(args.delete_entry):
                    if args.json:
                        self._log_json(
                            LOG_JSON_STATUS_ERROR,
                            f"Entry ID '{args.delete_entry}' does not exists",
                        )

                    else:
                        self._log_stdout(
                            f"Entry ID '{args.delete_entry}' does not exists",
                            color=Colors.RED,
                            error=True,
                        )

                    return -1

                access_token_manager.deleteEntry(args.delete_entry)

        return 0

    def regen_rsa(self):
        parser = argparse.ArgumentParser(
            description="| Regenerate RSA keys",
            usage=f"{sys.argv[0]} regen-rsa [OPT]",
        )
        parser.add_argument(
            "-b",
            help=f"specify the key size, in bytes (default is {DEFAULT_RSA_KEY_SIZE})",
            dest="key_size",
            type=int,
        )
        parser.add_argument(
            "--json", help="print output in JSON format", action="store_true"
        )
        args = parser.parse_args(sys.argv[2:])

        self.json = args.json

        new_rsa_wrapper = RSAWrapper(
            key_size=args.key_size if args.key_size else DEFAULT_RSA_KEY_SIZE
        )

        with open(self.config_content.get("private_rsa_key_file_path"), "w") as fd:
            fd.write(new_rsa_wrapper.getPrivateKey().decode())

        with open(self.config_content.get("public_rsa_key_file_path"), "w") as fd:
            fd.write(new_rsa_wrapper.getPublicKey().decode())

        fingerprint = hashlib.sha256(new_rsa_wrapper.getPublicKey()).hexdigest()

        if args.json:
            self._log_json(
                LOG_JSON_STATUS_SUCCESS,
                "RSA keys re-generated",
                result={"fingerprint": fingerprint},
            )

        else:
            self._log_stdout("RSA keys re-generated", color=Colors.GREEN)
            self._log_stdout(f"  Fingerprint : {fingerprint}")

        return 0
