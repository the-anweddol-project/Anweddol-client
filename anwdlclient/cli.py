"""
    Copyright 2023 The Anweddol project
    See the LICENSE file for licensing informations
    ---

    CLI : Main anwdlclient CLI

    @IDEA : TOR func ?
    import socket
    import socks

    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
    s = socks.socksocket()
    s.connect(('anguilla.debian.or.at', 1234))
    s.sendall('Hello world')
    print(s.recv(1024))

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
from .core.util import isValidIP
from .core.client import (
    ClientInterface,
    DEFAULT_SERVER_LISTEN_PORT,
    REQUEST_VERB_CREATE,
    REQUEST_VERB_DESTROY,
    REQUEST_VERB_STAT,
)
from .tools.credentials import SessionCredentialsManager, ContainerCredentialsManager
from .tools.accesstk import AccessTokenManager
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


class MainAnweddolClientCLI:
    def __init__(self):
        self.json = False

        try:
            if not os.path.exists(CONFIG_FILE_PATH):
                print(
                    f"\nx> The configuration file {CONFIG_FILE_PATH} was not found on system\n",
                    file=sys.stderr,
                )
                exit(-1)

            self.config_manager = ConfigurationFileManager(CONFIG_FILE_PATH)
            self.config_content = self.config_manager.loadContent()

            if not self.config_content[0]:
                print(
                    "Error in configuration file :\n",
                    file=sys.stderr,
                )
                print(json.dumps(self.config_content[1], indent=4), file=sys.stderr)
                exit(-1)

            self.config_content = self.config_content[1]

        except Exception as E:
            print(
                f"\nx> An error occured during configuration file processing : {E}\n",
                file=sys.stderr,
            )
            exit(-1)

        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage=f"""{sys.argv[0]} <command> [OPT] 

The Anweddol client CLI implementation.
Interact with Anweddol servers and manage session/containers credentials.

Version {__version__}

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
            getattr(self, args.command.replace("-", "_"))()
            exit(0)

        except KeyboardInterrupt:
            exit(0)

        except Exception as E:
            if self.json:
                self.__log_json(
                    LOG_JSON_STATUS_ERROR, "An error occured", data={"error": str(E)}
                )

            else:
                self.__log_stdout(f"Error : {E}\n")

            exit(-1)

    def __regen_rsa_keys(self, rsa_wrapper):
        if not os.path.exists(self.config_content.get("rsa_keys_root_path")):
            os.mkdir(self.config_content.get("rsa_keys_root_path"))

        with open(
            self.config_content.get("rsa_keys_root_path")
            + "/"
            + PRIVATE_PEM_KEY_FILENAME,
            "w",
        ) as fd:
            fd.write(rsa_wrapper.getPrivateKey().decode())

        with open(
            self.config_content.get("rsa_keys_root_path")
            + "/"
            + PUBLIC_PEM_KEY_FILENAME,
            "w",
        ) as fd:
            fd.write(rsa_wrapper.getPublicKey().decode())

        return hashlib.sha256(rsa_wrapper.getPublicKey()).hexdigest()

    def __load_rsa_keys(self):
        self.runtime_rsa_wrapper = None

        if not self.config_content.get("enable_onetime_rsa_keys"):
            if not os.path.exists(self.config_content.get("rsa_keys_root_path")):
                os.mkdir(self.config_content.get("rsa_keys_root_path"))

            if not os.path.exists(
                self.config_content.get("rsa_keys_root_path")
                + "/"
                + PRIVATE_PEM_KEY_FILENAME
            ):
                self.runtime_rsa_wrapper = RSAWrapper()

                with open(
                    self.config_content.get("rsa_keys_root_path")
                    + "/"
                    + PUBLIC_PEM_KEY_FILENAME,
                    "w",
                ) as fd:
                    fd.write(self.runtime_rsa_wrapper.getPublicKey().decode())

                with open(
                    self.config_content.get("rsa_keys_root_path")
                    + "/"
                    + PRIVATE_PEM_KEY_FILENAME,
                    "w",
                ) as fd:
                    fd.write(self.runtime_rsa_wrapper.getPrivateKey().decode())

            else:
                self.runtime_rsa_wrapper = RSAWrapper(generate_key_pair=False)

                with open(
                    self.config_content.get("rsa_keys_root_path")
                    + "/"
                    + PUBLIC_PEM_KEY_FILENAME,
                    "r",
                ) as fd:
                    self.runtime_rsa_wrapper.setPublicKey(fd.read().encode())

                with open(
                    self.config_content.get("rsa_keys_root_path")
                    + "/"
                    + PRIVATE_PEM_KEY_FILENAME,
                    "r",
                ) as fd:
                    self.runtime_rsa_wrapper.setPrivateKey(fd.read().encode())

    def __log_stdout(self, message, bypass=False):
        if not bypass:
            print(message)

    def __log_json(self, status, message, data={}):
        print(json.dumps({"status": status, "message": message, "data": data}))

    def __create_file_recursively(self, path, is_folder=False):
        try:
            os.makedirs(os.path.dirname(path) if not is_folder else path)

        except FileExistsError:
            pass

        if is_folder:
            return

        with open(path, "w") as fd:
            fd.close()

    def create(self):
        parser = argparse.ArgumentParser(
            description="-> Create a container on a remote server",
            usage=f"""{sys.argv[0]} create <ip> [OPT]""",
        )
        parser.add_argument("ip", help="specify the server IP", type=str)
        parser.add_argument(
            "-p", "--port", help="specify the server listen port", type=int
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

        self.__load_rsa_keys()

        if not isValidIP(args.ip):
            if args.json:
                self.__log_json(
                    LOG_JSON_STATUS_ERROR,
                    f"'{args.ip}' is not a valid IPv4 ip format",
                )
                return

            self.__log_stdout(f"'{args.ip}' is not a valid IPv4 ip format\n")
            return

        if args.port:
            if args.port >= 65535 or args.port <= 0:
                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_ERROR,
                        f"'{args.port}' is not a non-zero integer less than 65535",
                    )
                    return

                self.__log_stdout(
                    f"'{args.port}' is not a non-zero integer less than 65535\n"
                )
                return

        if not os.path.exists(self.config_content.get("access_token_db_file_path")):
            self.__create_file_recursively(
                self.config_content.get("access_token_db_file_path")
            )

        if not os.path.exists(
            self.config_content.get("session_credentials_db_file_path")
        ):
            self.__create_file_recursively(
                self.config_content.get("session_credentials_db_file_path")
            )

        if not os.path.exists(
            self.config_content.get("container_credentials_db_file_path")
        ):
            self.__create_file_recursively(
                self.config_content.get("container_credentials_db_file_path")
            )

        access_token_manager = AccessTokenManager(
            self.config_content.get("access_token_db_file_path")
        )
        session_credentials_manager = SessionCredentialsManager(
            self.config_content.get("session_credentials_db_file_path")
        )
        container_credentials_manager = ContainerCredentialsManager(
            self.config_content.get("container_credentials_db_file_path")
        )
        client = ClientInterface(
            args.ip,
            server_listen_port=args.port if args.port else DEFAULT_SERVER_LISTEN_PORT,
            rsa_wrapper=self.runtime_rsa_wrapper,
            auto_connect=False,
        )

        try:
            client.connectServer()

            request_parameters = {}

            for entries in access_token_manager.listEntries():
                if args.ip == entries[2]:
                    request_parameters.update(
                        {"access_token": access_token_manager.getEntry(entries[0])[4]}
                    )

            client.sendRequest(REQUEST_VERB_CREATE, parameters=request_parameters)

            resp = client.recvResponse()
            client.closeConnection()

            if not resp[0]:
                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_ERROR,
                        "Received invalid response",
                        data={"error_dict": resp[1]},
                    )
                    return

                self.__log_stdout(
                    f"Received invalid response : {json.dumps(resp[1], indent=4)}\n"
                )
                return

            if not resp[1]["success"]:
                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_ERROR,
                        "Failed to create container",
                        data={"response": resp[1]},
                    )
                    return

                self.__log_stdout(
                    f"Failed to create container : {resp[1]['message']}\n"
                )
                return

            self.__log_stdout("Container successfully created", bypass=args.json)
            self.__log_stdout(f" ↳ Message : {resp[1]['message']}", bypass=args.json)
            self.__log_stdout(
                f" ↳ Container ISO checksum : {resp[1]['data'].get('container_iso_sha256')}",
                bypass=args.json,
            )

            if args.show_credentials:
                self.__log_stdout("Session credentials :", bypass=args.json)
                self.__log_stdout(
                    f" ↳ Container UUID : {resp[1]['data'].get('container_uuid')}",
                    bypass=args.json,
                )
                self.__log_stdout(
                    f" ↳ Client token : {resp[1]['data'].get('client_token')}",
                    bypass=args.json,
                )
                self.__log_stdout(
                    f" ↳ Container username : {resp[1]['data'].get('container_username')}",
                    bypass=args.json,
                )
                self.__log_stdout(
                    f" ↳ Container password : {resp[1]['data'].get('container_password')}",
                    bypass=args.json,
                )
                self.__log_stdout(
                    f" ↳ Container listen port : {resp[1]['data'].get('container_listen_port')}\n",
                    bypass=args.json,
                )

            if not args.do_not_store:
                new_session_credentials_entry_tuple = (
                    session_credentials_manager.addEntry(
                        args.ip,
                        args.port if args.port else DEFAULT_SERVER_LISTEN_PORT,
                        resp[1]["data"].get("container_uuid"),
                        resp[1]["data"].get("client_token"),
                    )
                )

                new_container_credentials_entry_tuple = (
                    container_credentials_manager.addEntry(
                        args.ip,
                        args.port if args.port else DEFAULT_SERVER_LISTEN_PORT,
                        resp[1]["data"].get("container_username"),
                        resp[1]["data"].get("container_password"),
                        resp[1]["data"].get("container_listen_port"),
                    )
                )

            access_token_manager.closeDatabase()
            session_credentials_manager.closeDatabase()
            container_credentials_manager.closeDatabase()

            if args.json:
                data_dict = {
                    "message": resp[1]["message"],
                    "session_entry_id": new_session_credentials_entry_tuple[0],
                    "container_entry_id": new_container_credentials_entry_tuple[0],
                }
                data_dict.update(resp[1]["data"])

                self.__log_json(
                    LOG_JSON_STATUS_SUCCESS,
                    "Container successfully created",
                    data=data_dict,
                )

                return

            self.__log_stdout(
                f"Session credentials was stored with ID {new_session_credentials_entry_tuple[0]}",
            )
            self.__log_stdout(
                f"Container credentials was stored with ID {new_container_credentials_entry_tuple[0]}\n",
            )

        except Exception as E:
            if not client.isClosed():
                client.closeConnection()

            access_token_manager.closeDatabase()
            session_credentials_manager.closeDatabase()
            container_credentials_manager.closeDatabase()

            raise E

    def destroy(self):
        parser = argparse.ArgumentParser(
            description="-> Destroy a created container on a remote server",
            usage=f"{sys.argv[0]} destroy <session_entry_id> [OPT] ",
        )
        parser.add_argument(
            "session_entry_id", help="specify the local session ID", type=int
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

        self.__load_rsa_keys()

        if not os.path.exists(self.config_content.get("access_token_db_file_path")):
            self.__create_file_recursively(
                self.config_content.get("access_token_db_file_path")
            )

        if not os.path.exists(
            self.config_content.get("session_credentials_db_file_path")
        ):
            self.__create_file_recursively(
                self.config_content.get("session_credentials_db_file_path")
            )

        if not os.path.exists(
            self.config_content.get("container_credentials_db_file_path")
        ):
            self.__create_file_recursively(
                self.config_content.get("container_credentials_db_file_path")
            )

        access_token_manager = AccessTokenManager(
            self.config_content.get("access_token_db_file_path")
        )
        session_credentials_manager = SessionCredentialsManager(
            self.config_content.get("session_credentials_db_file_path")
        )
        container_credentials_manager = ContainerCredentialsManager(
            self.config_content.get("container_credentials_db_file_path")
        )
        client = None

        try:
            credentials_content = session_credentials_manager.getEntry(
                args.session_entry_id
            )

            if not credentials_content:
                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_ERROR,
                        f"Session ID '{args.session_entry_id}' does not exists",
                    )
                    return

                self.__log_stdout(
                    f"Session ID '{args.session_entry_id}' does not exists\n"
                )
                return

            client = ClientInterface(
                credentials_content[2],
                server_listen_port=credentials_content[3],
                rsa_wrapper=self.runtime_rsa_wrapper,
            )

            request_parameters = {
                "container_uuid": credentials_content[4],
                "client_token": credentials_content[5],
            }

            for entries in access_token_manager.listEntries():
                if credentials_content[2] == entries[2]:
                    request_parameters.update(
                        {"access_token": access_token_manager.getEntry(entries[0])[4]}
                    )

            client.sendRequest(REQUEST_VERB_DESTROY, parameters=request_parameters)

            resp = client.recvResponse()
            client.closeConnection()

            if not resp[0]:
                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_ERROR,
                        "Received invalid response",
                        data={"error_dict": resp[1]},
                    )
                    return

                self.__log_stdout(
                    f"Received invalid response : {json.dumps(resp[1], indent=4)}\n"
                )
                return

            if not resp[1]["success"]:
                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_ERROR,
                        "Failed to destroy container",
                        data={"response": resp[1]},
                    )
                    return

                self.__log_stdout(
                    f"Failed to destroy container : {resp[1]['message']}\n"
                )
                return

            if not args.do_not_delete:
                session_credentials_manager.deleteEntry(args.session_entry_id)

                container_entry_id = container_credentials_manager.getEntryID(
                    credentials_content[2]
                )

                if container_entry_id:
                    container_credentials_manager.deleteEntry(container_entry_id)

            access_token_manager.closeDatabase()
            session_credentials_manager.closeDatabase()
            container_credentials_manager.closeDatabase()

            if args.json:
                self.__log_json(
                    LOG_JSON_STATUS_SUCCESS,
                    "Container successfully destroyed",
                    data={"message": resp[1]["message"]},
                )
                return

            self.__log_stdout("Container successfully destroyed")
            self.__log_stdout(f" ↳ Message : {resp[1]['message']}\n")

        except Exception as E:
            if client and not client.isClosed():
                client.closeConnection()

            access_token_manager.closeDatabase()
            session_credentials_manager.closeDatabase()
            container_credentials_manager.closeDatabase()

            raise E

    def stat(self):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="""-> Retrieve runtime statistics of a remote server

Get the actual server uptime and the available containers left amount.""",
            usage=f"{sys.argv[0]} stat <ip> [OPT] ",
        )

        parser.add_argument("ip", help="specify the server IP", type=str)
        parser.add_argument(
            "-p", "--port", help="specify the server listen port", type=int
        )
        parser.add_argument(
            "--json", help="print output in JSON format", action="store_true"
        )
        args = parser.parse_args(sys.argv[2:])

        self.json = args.json

        self.__load_rsa_keys()

        if not isValidIP(args.ip):
            if args.json:
                self.__log_json(
                    LOG_JSON_STATUS_ERROR,
                    f"'{args.ip}' is not a valid IPv4 ip format",
                )
                return

            self.__log_stdout(f"'{args.ip}' is not a valid IPv4 ip format\n")
            return

        if args.port:
            if args.port >= 65535 or args.port <= 0:
                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_ERROR,
                        f"'{args.port}' is not a non-zero integer less than 65535",
                    )
                    return

                self.__log_stdout(
                    f"'{args.port}' is not a non-zero integer less than 65535\n"
                )
                return

        if not os.path.exists(self.config_content.get("access_token_db_file_path")):
            self.__create_file_recursively(
                self.config_content.get("access_token_db_file_path")
            )

        access_token_manager = AccessTokenManager(
            self.config_content.get("access_token_db_file_path")
        )
        client = ClientInterface(
            args.ip,
            server_listen_port=args.port if args.port else DEFAULT_SERVER_LISTEN_PORT,
            rsa_wrapper=self.runtime_rsa_wrapper,
            auto_connect=False,
        )

        try:
            client.connectServer()

            request_parameters = {}

            for entries in access_token_manager.listEntries():
                if args.ip == entries[2]:
                    request_parameters.update(
                        {"access_token": access_token_manager.getEntry(entries[0])[4]}
                    )

            client.sendRequest(REQUEST_VERB_STAT, parameters=request_parameters)

            resp = client.recvResponse()
            client.closeConnection()

            if not resp[0]:
                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_ERROR,
                        "Received invalid response",
                        data={"error_dict": resp[1]},
                    )
                    return

                self.__log_stdout(
                    f"Received invalid response : {json.dumps(resp[1], indent=4)}\n"
                )
                return

            if not resp[1]["success"]:
                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_ERROR,
                        "Failed to stat server",
                        data={"response": resp[1]},
                    )
                    return

                self.__log_stdout(f"Failed to stat server : {resp[1]['message']}\n")
                return

            if args.json:
                data_dict = {"message": resp[1]["message"]}
                data_dict.update(resp[1]["data"])

                self.__log_json(
                    LOG_JSON_STATUS_SUCCESS,
                    "Server statistics",
                    data=data_dict,
                )
                return

            self.__log_stdout("Server statistics :")
            self.__log_stdout(f" ↳ Uptime : {resp[1]['data'].get('uptime')}")
            self.__log_stdout(
                f" ↳ Available containers : {resp[1]['data'].get('available')}\n"
            )

            access_token_manager.closeDatabase()

        except Exception as E:
            if not client.isClosed():
                client.closeConnection()

            access_token_manager.closeDatabase()
            raise E

    def session(self):
        parser = argparse.ArgumentParser(
            description="-> Manage stored session credentials",
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

        if not os.path.exists(
            self.config_content.get("session_credentials_db_file_path")
        ):
            self.__create_file_recursively(
                self.config_content.get("session_credentials_db_file_path")
            )

        session_credentials_manager = SessionCredentialsManager(
            self.config_content.get("session_credentials_db_file_path")
        )

        try:
            if args.l:
                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_SUCCESS,
                        "Recorded entries ID",
                        data={"entry_list": session_credentials_manager.listEntries()},
                    )
                    return

                for entries in session_credentials_manager.listEntries():
                    self.__log_stdout(f"Entry ID {entries[0]}")
                    self.__log_stdout(
                        f" ↳ Created : {datetime.fromtimestamp(entries[1])}"
                    )
                    self.__log_stdout(f" ↳ Server IP : {entries[2]}\n")

            elif args.get_entry:
                credentials = session_credentials_manager.getEntry(args.get_entry)

                if not credentials:
                    session_credentials_manager.closeDatabase()

                    if args.json:
                        self.__log_json(
                            LOG_JSON_STATUS_ERROR,
                            f"Entry ID '{args.get_entry}' does not exists",
                        )
                        return

                    self.__log_stdout(f"Entry ID '{args.get_entry}' does not exists\n")
                    return

                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_SUCCESS,
                        "Entry ID content",
                        data={
                            "created": credentials[1],
                            "server_ip": credentials[2],
                            "server_port": credentials[3],
                            "container_uuid": credentials[4],
                            "client_token": credentials[5],
                        },
                    )
                    return

                self.__log_stdout(f"Entry ID {args.get_entry} content :")
                self.__log_stdout(
                    f" ↳ Created : {datetime.fromtimestamp(credentials[1])}"
                )
                self.__log_stdout(f" ↳ Server IP : {credentials[2]}")
                self.__log_stdout(f" ↳ Server port : {credentials[3]}")
                self.__log_stdout(f" ↳ Container UUID : {credentials[4]}")
                self.__log_stdout(f" ↳ Client token : {credentials[5]}\n")

            else:
                if args.delete_entry:
                    if not session_credentials_manager.getEntry(args.delete_entry):
                        session_credentials_manager.closeDatabase()

                        if args.json:
                            self.__log_json(
                                LOG_JSON_STATUS_ERROR,
                                f"Entry ID '{args.delete_entry}' does not exists",
                            )
                            return

                        self.__log_stdout(
                            f"Entry ID '{args.delete_entry}' does not exists\n"
                        )
                        return

                    session_credentials_manager.deleteEntry(args.delete_entry)

                    if args.json:
                        self.__log_json(LOG_JSON_STATUS_SUCCESS, "Entry ID was deleted")
                        return

                    self.__log_stdout(f"Entry ID {args.delete_entry} was deleted\n")

            session_credentials_manager.closeDatabase()

        except Exception as E:
            session_credentials_manager.closeDatabase()
            raise E

    def container(self):
        parser = argparse.ArgumentParser(
            description="-> Manage stored container credentials",
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

        if not os.path.exists(
            self.config_content.get("container_credentials_db_file_path")
        ):
            self.__create_file_recursively(
                self.config_content.get("container_credentials_db_file_path")
            )

        container_credentials_manager = ContainerCredentialsManager(
            self.config_content.get("container_credentials_db_file_path")
        )

        try:
            if args.l:
                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_SUCCESS,
                        "Recorded entries ID",
                        data={
                            "entry_list": container_credentials_manager.listEntries()
                        },
                    )
                    return

                for entries in container_credentials_manager.listEntries():
                    self.__log_stdout(f"Entry ID {entries[0]}")
                    self.__log_stdout(
                        f" ↳ Created : {datetime.fromtimestamp(entries[1])}"
                    )
                    self.__log_stdout(f" ↳ Server IP : {entries[2]}\n")

            elif args.get_entry:
                credentials = container_credentials_manager.getEntry(args.get_entry)

                if not credentials:
                    container_credentials_manager.closeDatabase()
                    if args.json:
                        self.__log_json(
                            LOG_JSON_STATUS_ERROR,
                            f"Entry ID '{args.get_entry}' does not exists",
                        )
                        return

                    self.__log_stdout(f"Entry ID '{args.get_entry}' does not exists\n")
                    return

                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_SUCCESS,
                        "Entry ID content",
                        data={
                            "created": credentials[1],
                            "server_ip": credentials[2],
                            "server_port": credentials[3],
                            "container_username": credentials[4],
                            "container_password": credentials[5],
                            "container_listen_port": credentials[6],
                        },
                    )
                    return

                self.__log_stdout(f"Entry ID {args.get_entry} content :")
                self.__log_stdout(
                    f" ↳ Created : {datetime.fromtimestamp(credentials[1])}"
                )
                self.__log_stdout(f" ↳ Server IP : {credentials[2]}")
                self.__log_stdout(f" ↳ Server port : {credentials[3]}")
                self.__log_stdout(f" ↳ Container SSH username : {credentials[4]}")
                self.__log_stdout(f" ↳ Container SSH password : {credentials[5]}")
                self.__log_stdout(f" ↳ Container SSH listen port : {credentials[6]}\n")

            else:
                if args.delete_entry:
                    if not container_credentials_manager.getEntry(args.delete_entry):
                        container_credentials_manager.closeDatabase()

                        if args.json:
                            self.__log_json(
                                LOG_JSON_STATUS_ERROR,
                                f"Entry ID '{args.delete_entry}' does not exists",
                            )
                            return

                        self.__log_stdout(
                            f"Entry ID '{args.delete_entry}' does not exists\n"
                        )
                        return

                    container_credentials_manager.deleteEntry(args.delete_entry)

                    if args.json:
                        self.__log_json(LOG_JSON_STATUS_SUCCESS, "Entry ID was deleted")
                        return

                    self.__log_stdout(f"Entry ID {args.delete_entry} was deleted\n")

            container_credentials_manager.closeDatabase()

        except Exception as E:
            container_credentials_manager.closeDatabase()
            raise E

    def access_tk(self):
        parser = argparse.ArgumentParser(
            description="-> Manage access tokens",
            usage=f"{sys.argv[0]} access-tk [OPT] ",
            epilog="(*) Input pipe is needed if used with the --json flag : 'echo <token> | anwdlclient access-tk -a <server_ip> --json'",
        )
        parser.add_argument(
            "-l", help="list recorded tokens entries", action="store_true"
        )
        parser.add_argument(
            "-a",
            help="add entry token (*)",
            dest="server_ip",
            type=str,
        )
        parser.add_argument(
            "-p",
            help="print entry token",
            dest="print_entry",
            metavar="ENTRY_ID",
            type=int,
        )
        parser.add_argument(
            "-d",
            help="delete entry token",
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

        if not os.path.exists(self.config_content.get("access_token_db_file_path")):
            self.__create_file_recursively(
                self.config_content.get("access_token_db_file_path")
            )

        access_token_manager = AccessTokenManager(
            self.config_content.get("access_token_db_file_path")
        )

        try:
            if args.l:
                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_SUCCESS,
                        "Recorded entries ID",
                        data={"entry_list": access_token_manager.listEntries()},
                    )
                    return

                for entries in access_token_manager.listEntries():
                    self.__log_stdout(f"Entry ID {entries[0]}")
                    self.__log_stdout(
                        f" ↳ Created : {datetime.fromtimestamp(entries[1])}"
                    )
                    self.__log_stdout(f" ↳ Server IP : {entries[2]}\n")

            elif args.server_ip:
                if not isValidIP(args.server_ip):
                    if args.json:
                        self.__log_json(
                            LOG_JSON_STATUS_ERROR,
                            f"'{args.server_ip}' is not a valid IPv4 ip format",
                        )
                        return

                    self.__log_stdout(
                        f"'{args.server_ip}' is not a valid IPv4 ip format\n"
                    )
                    return

                if access_token_manager.getEntryID(args.server_ip):
                    if args.json:
                        self.__log_json(
                            LOG_JSON_STATUS_ERROR,
                            f"'{args.server_ip}' is already specified on database",
                        )
                        return

                    self.__log_stdout(
                        f"'{args.server_ip}' is already specified on database\n"
                    )
                    return

                new_access_token = (
                    getpass(prompt="Paste the new token : ")
                    if not args.json
                    else input("")
                )
                new_entry_tuple = access_token_manager.addEntry(
                    args.server_ip,
                    args.server_port
                    if args.server_port
                    else DEFAULT_SERVER_LISTEN_PORT,
                    new_access_token,
                )

                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_SUCCESS,
                        "New token entry created",
                        data={"entry_id": new_entry_tuple[0]},
                    )
                    return

                self.__log_stdout(
                    f"New token entry created (Entry ID : {new_entry_tuple[0]})\n"
                )

            elif args.print_entry:
                entry_content = access_token_manager.getEntry(args.print_entry)

                if not entry_content:
                    access_token_manager.closeDatabase()

                    if args.json:
                        self.__log_json(
                            LOG_JSON_STATUS_ERROR,
                            f"Entry ID '{args.print_entry}' does not exists",
                        )
                        return

                    self.__log_stdout(
                        f"Entry ID '{args.print_entry}' does not exists\n"
                    )
                    return

                if args.json:
                    self.__log_json(
                        LOG_JSON_STATUS_SUCCESS,
                        "Entry ID content",
                        data={
                            "created": entry_content[1],
                            "server_ip": entry_content[2],
                            "server_port": entry_content[3],
                            "access_token": entry_content[4],
                        },
                    )
                    return

                self.__log_stdout(f"Entry ID {args.print_entry} content :")
                self.__log_stdout(
                    f" ↳ Created : {datetime.fromtimestamp(entry_content[1])}"
                )
                self.__log_stdout(f" ↳ Server IP : {entry_content[2]}")
                self.__log_stdout(f" ↳ Server port : {entry_content[3]}")
                self.__log_stdout(f" ↳ Access token : {entry_content[4]}\n")

            else:
                if args.delete_entry:
                    if not access_token_manager.getEntry(args.delete_entry):
                        access_token_manager.closeDatabase()

                        if args.json:
                            self.__log_json(
                                LOG_JSON_STATUS_ERROR,
                                f"Entry ID '{args.delete_entry}' does not exists",
                            )
                            return

                        self.__log_stdout(
                            f"Entry ID '{args.delete_entry}' does not exists\n"
                        )
                        return

                    access_token_manager.deleteEntry(args.delete_entry)

                    if args.json:
                        self.__log_json(LOG_JSON_STATUS_SUCCESS, "Entry ID was deleted")
                        return

                    self.__log_stdout(f"Entry ID {args.delete_entry} was deleted\n")

            access_token_manager.closeDatabase()

        except Exception as E:
            access_token_manager.closeDatabase()
            raise E

    def regen_rsa(self):
        parser = argparse.ArgumentParser(
            description="-> Regenerate RSA keys",
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
        fingerprint = self.__regen_rsa_keys(new_rsa_wrapper)

        if args.json:
            self.__log_json(
                LOG_JSON_STATUS_SUCCESS,
                "RSA keys re-generated",
                data={"fingerprint": fingerprint},
            )
            return

        self.__log_stdout("RSA keys re-generated")
        self.__log_stdout(f" ↳ Fingerprint : {fingerprint}\n")
