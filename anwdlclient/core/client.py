"""
    Copyright 2023 The Anweddol project
    See the LICENSE file for licensing informations
    ---

    Client functionnality

"""
import socket
import json

from .crypto import RSAWrapper, AESWrapper
from .sanitize import makeRequest, verifyResponseContent


# Default parameters
DEFAULT_SERVER_LISTEN_PORT = 6150
DEFAULT_CLIENT_TIMEOUT = 10

DEFAULT_AUTO_CONNECT = True
DEFAULT_RECEIVE_FIRST = False


# Constants definition
MESSAGE_OK = "1"
MESSAGE_NOK = "0"

REQUEST_VERB_CREATE = "CREATE"
REQUEST_VERB_DESTROY = "DESTROY"
REQUEST_VERB_STAT = "STAT"

RESPONSE_MSG_OK = "OK"
RESPONSE_MSG_BAD_AUTH = "Bad authentification"
RESPONSE_MSG_BAD_REQ = "Bad request"
RESPONSE_MSG_REFUSED_REQ = "Refused request"
RESPONSE_MSG_UNAVAILABLE = "Unavailable"
RESPONSE_MSG_INTERNAL_ERROR = "Internal error"


class ClientInterface:
    def __init__(
        self,
        server_ip: str = None,
        server_listen_port: int = DEFAULT_SERVER_LISTEN_PORT,
        timeout: int = DEFAULT_CLIENT_TIMEOUT,
        rsa_wrapper: RSAWrapper = None,
        aes_wrapper: AESWrapper = None,
        auto_connect: bool = DEFAULT_AUTO_CONNECT,
    ):
        self.is_closed = True
        self.socket = None
        self.server_ip = server_ip
        self.server_port = server_listen_port
        self.rsa_wrapper = rsa_wrapper if rsa_wrapper else RSAWrapper()
        self.aes_wrapper = aes_wrapper if aes_wrapper else AESWrapper()

        if auto_connect:
            self.connectServer()

    def __del__(self):
        if not self.is_closed:
            self.closeConnection()

    def isClosed(self) -> bool:
        return self.is_closed

    def getSocketDescriptor(self) -> socket.socket:
        return self.socket

    def getRSAWrapper(self) -> RSAWrapper:
        return self.rsa_wrapper

    def getAESWrapper(self) -> AESWrapper:
        return self.aes_wrapper

    def setRSAWrapper(self, rsa_wrapper: RSAWrapper) -> None:
        self.rsa_wrapper = rsa_wrapper

    def setAESWrapper(self, aes_wrapper: AESWrapper) -> None:
        self.aes_wrapper = aes_wrapper

    def connectServer(self, receive_first: bool = DEFAULT_RECEIVE_FIRST) -> None:
        if not self.is_closed:
            raise RuntimeError("Connection is already active")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_ip, self.server_port))
        self.is_closed = False

        if receive_first:
            self.recvPublicRSAKey()
            self.sendPublicRSAKey()
            self.recvAESKey()
            self.sendAESKey()

        else:
            self.sendPublicRSAKey()
            self.recvPublicRSAKey()
            self.sendAESKey()
            self.recvAESKey()

    def sendPublicRSAKey(self) -> None:
        if self.is_closed:
            raise RuntimeError("Client must be connected to the server")

        rsa_public_key = self.rsa_wrapper.getPublicKey()
        rsa_public_key_length = str(len(rsa_public_key))

        # Send the key size
        self.socket.sendall(
            (rsa_public_key_length + ("=" * (8 - len(rsa_public_key_length)))).encode()
        )

        if self.socket.recv(1).decode() is not MESSAGE_OK:
            raise RuntimeError("Peer refused the packet")

        self.socket.sendall(rsa_public_key)

        if self.socket.recv(1).decode() is not MESSAGE_OK:
            raise RuntimeError("Peer refused the RSA key")

    def recvPublicRSAKey(self) -> None:
        if self.is_closed:
            raise RuntimeError("Client must be connected to the server")

        try:
            recv_key_length = int(self.socket.recv(8).decode().split("=")[0])

            if recv_key_length <= 0:
                self.socket.sendall(MESSAGE_NOK.encode())
                raise ValueError(f"Received bad key length : {recv_key_length}")

            self.socket.sendall(MESSAGE_OK.encode())

            recv_packet = self.socket.recv(recv_key_length)

            self.rsa_wrapper.setRemotePublicKey(recv_packet)
            self.socket.sendall(MESSAGE_OK.encode())

        except Exception as E:
            self.socket.sendall(MESSAGE_NOK.encode())
            raise E

    def sendAESKey(self) -> None:
        if self.is_closed:
            raise RuntimeError("Client must be connected to the server")

        if not self.rsa_wrapper:
            raise ValueError("RSA cipher is not set")

        aes_key = self.aes_wrapper.getKey()
        aes_iv = self.aes_wrapper.getIv()

        self.socket.sendall(
            self.rsa_wrapper.encryptData(aes_key + aes_iv, encode=False)
        )

        if self.socket.recv(1).decode() is not MESSAGE_OK:
            raise RuntimeError("Peer refused the AES key")

    def recvAESKey(self) -> None:
        try:
            if self.is_closed:
                raise RuntimeError("Client must be connected to the server")

            if not self.rsa_wrapper:
                raise ValueError("RSA cipher is not set")

            # Key size is divided by 8 to get the supported block size
            recv_packet = self.rsa_wrapper.decryptData(
                self.socket.recv(int(self.rsa_wrapper.getKeySize() / 8)),
                decode=False,
            )

            self.aes_wrapper.setKey(recv_packet[:-16], recv_packet[-16:])

            self.socket.sendall(MESSAGE_OK.encode())

        except Exception as E:
            self.socket.sendall(MESSAGE_NOK.encode())
            raise E

    def sendRequest(self, verb: str, parameters: dict = {}) -> None:
        if self.is_closed:
            raise RuntimeError("Client must be connected to the server")

        if not self.aes_wrapper:
            raise ValueError("AES cipher is not set")

        request_tuple = makeRequest(verb, parameters=parameters)

        if not request_tuple[0]:
            raise ValueError(f"Error in specified values : {request_tuple[1]}")

        encrypted_packet = self.aes_wrapper.encryptData(json.dumps(request_tuple[1]))

        packet_length = str(len(encrypted_packet))
        self.socket.sendall((packet_length + ("=" * (8 - len(packet_length)))).encode())

        if self.socket.recv(1).decode() != MESSAGE_OK:
            raise RuntimeError("Peer refused the packet")

        self.socket.sendall(encrypted_packet)

    def recvResponse(self) -> dict:
        if self.is_closed:
            raise RuntimeError("Client must be connected to the server")

        if not self.aes_wrapper:
            raise ValueError("AES cipher is not set")

        recv_packet_length = int(self.socket.recv(8).decode().split("=")[0])

        if recv_packet_length <= 0:
            self.socket.sendall(MESSAGE_NOK.encode())
            raise ValueError(
                f"Received bad packet length : {recv_packet_length}"
            )  # <----

        self.socket.sendall(MESSAGE_OK.encode())

        decrypted_recv_request = self.aes_wrapper.decryptData(
            self.socket.recv(recv_packet_length)
        )

        return verifyResponseContent(json.loads(decrypted_recv_request))

    def closeConnection(self) -> None:
        self.socket.close()
        self.is_closed = True
