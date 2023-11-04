"""
Copyright 2023 The Anweddol project
See the LICENSE file for licensing informations
---

This module provides the Anweddol client with normalized 
request / response values and formats verification features.

"""

import cerberus


def verifyResponseContent(response_dict: dict) -> tuple:
    validator = cerberus.Validator()
    validator.allow_unknown = True

    response_verification_scheme = {
        "success": {
            "type": "boolean",
            "required": True,
        },
        "message": {
            "type": "string",
            "required": True,
        },
        "data": {
            "type": "dict",
            "required": True,
            "schema": {
                "container_uuid": {
                    "type": "string",
                    "regex": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
                    "required": False,
                    "dependencies": [
                        "client_token",
                        "container_iso_sha256",
                        "container_username",
                        "container_password",
                        "container_listen_port",
                    ],
                },
                "client_token": {
                    "type": "string",
                    "regex": r"^[0-9a-zA-Z-_]{255}$",
                    "required": False,
                    "dependencies": [
                        "container_uuid",
                        "container_iso_sha256",
                        "container_username",
                        "container_password",
                        "container_listen_port",
                    ],
                },
                "container_iso_sha256": {
                    "type": "string",
                    "regex": r"^[a-f0-9]{64}$",
                    "required": False,
                    "dependencies": [
                        "container_uuid",
                        "client_token",
                        "container_username",
                        "container_password",
                        "container_listen_port",
                    ],
                },
                "container_username": {
                    "type": "string",
                    "regex": r"^user_[0-9]{5}$",
                    "required": False,
                    "dependencies": [
                        "container_uuid",
                        "client_token",
                        "container_iso_sha256",
                        "container_password",
                        "container_listen_port",
                    ],
                },
                "container_password": {
                    "type": "string",
                    "regex": r"^[a-zA-Z0-9]{1,}$",
                    "required": False,
                    "dependencies": [
                        "container_uuid",
                        "client_token",
                        "container_iso_sha256",
                        "container_username",
                        "container_listen_port",
                    ],
                },
                "container_listen_port": {
                    "type": "integer",
                    "required": False,
                    "min": 1,
                    "max": 65535,
                    "dependencies": [
                        "container_uuid",
                        "client_token",
                        "container_iso_sha256",
                        "container_username",
                        "container_password",
                    ],
                },
                "uptime": {
                    "type": "integer",
                    "required": False,
                    "dependencies": ["version"],
                    "min": 0,
                },
                "version": {
                    "type": "string",
                    "required": False,
                    "dependencies": ["uptime"],
                },
            },
        },
    }

    return (
        validator.validate(response_dict, response_verification_scheme),
        validator.document if validator.document else None,
        validator.errors if validator.errors else None,
    )


def makeRequest(verb: str, parameters: dict = {}) -> tuple:
    request_dict = {"verb": verb, "parameters": parameters}

    validator = cerberus.Validator()
    validator.allow_unknown = True

    request_verification_scheme = {
        "verb": {
            "type": "string",
            "regex": r"^[A-Z]{1,}$",
            "required": True,
        },
        "parameters": {
            "type": "dict",
            "required": True,
            "schema": {
                "container_uuid": {
                    "type": "string",
                    "regex": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
                    "required": False,
                    "dependencies": ["client_token"],
                },
                "client_token": {
                    "type": "string",
                    "regex": r"^[0-9a-zA-Z-_]{255}$",
                    "required": False,
                    "dependencies": ["container_uuid"],
                },
            },
        },
    }

    return (
        validator.validate(request_dict, request_verification_scheme),
        validator.document if validator.document else None,
        validator.errors if validator.errors else None,
    )
