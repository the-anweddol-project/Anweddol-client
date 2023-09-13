"""
    Copyright 2023 The Anweddol project
    See the LICENSE file for licensing informations
    ---

    CLI : Configuration file management features

"""
import cerberus
import yaml


class ConfigurationFileManager:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    # See the Cerberus docs : https://docs.python-cerberus.org/en/stable/usage.html
    def loadContent(self, auto_check: bool = True) -> None | dict:
        with open(self.config_file_path, "r") as fd:
            data = yaml.safe_load(fd)

        validator_schema_dict = {
            "session_credentials_db_file_path": {"type": "string", "required": True},
            "container_credentials_db_file_path": {"type": "string", "required": True},
            "access_token_db_file_path": {"type": "string", "required": True},
            "public_rsa_key_file_path": {"type": "string", "required": True},
            "private_rsa_key_file_path": {"type": "string", "required": True},
            "enable_onetime_rsa_keys": {"type": "boolean", "required": True},
        }

        validator = cerberus.Validator(purge_unknown=True)

        if not validator.validate(data, validator_schema_dict):
            return (False, validator.errors)

        return (True, validator.document)
