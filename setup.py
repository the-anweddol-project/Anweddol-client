"""
Copyright 2023 The Anweddol project
See the LICENSE file for licensing informations
---

Client installation script

"""

from subprocess import Popen, PIPE
from setuptools import setup
import getpass
import os

VERSION = "4.1.2"


def executeCommand(command):
    Popen(command.split(" "), shell=False, stdout=PIPE, stderr=PIPE)


def getReadmeContent():
    with open("README.md", "r") as fd:
        return fd.read()


anweddol_base_path = (
    f"C:\\Users\\{getpass.getuser()}\\Anweddol\\"
    if os.name == "nt"
    else f"/home/{getpass.getuser()}/.anweddol/"
)
local_ifs = "\\" if os.name == "nt" else "/"

print("[SETUP] Creating base folder ...")
if not os.path.exists(anweddol_base_path):
    os.mkdir(anweddol_base_path)

print("[SETUP] Creating configuration file ...")
if os.path.exists(anweddol_base_path + "config.yaml"):
    os.remove(anweddol_base_path + "config.yaml")

# Manually assemble the configuration file content depending of the environment
config_file_content = """# Configuration file for Anweddol client
#
# This document contains all of the configurations that the client 
# will be using. Comment or un-comment variables to change their 
# default values. Refer to the units explanations below, 
# and the official anweddol client documentation.

# Credentials database path
session_credentials_db_file_path: {}
container_credentials_db_file_path: {}
access_token_db_file_path: {}

# RSA keys root path
public_rsa_key_file_path: {}
private_rsa_key_file_path: {}

# Generate RSA key pair on start and ignore the stored one
# Enabled by default for privacy matters
enable_onetime_rsa_keys: True
""".format(
    f"{anweddol_base_path}credentials{local_ifs}core{local_ifs}session_credentials.db",
    f"{anweddol_base_path}credentials{local_ifs}core{local_ifs}container_credentials.db",
    f"{anweddol_base_path}credentials{local_ifs}access_token.db",
    f"{anweddol_base_path}rsa{local_ifs}public.pem",
    f"{anweddol_base_path}rsa{local_ifs}private.pem",
)

with open(anweddol_base_path + "config.yaml", "w") as fd:
    fd.write(config_file_content)

print("[SETUP] Installing Anweddol client ...")
setup(
    name="anwdlclient",
    version=VERSION,
    author="The Anweddol project",
    author_email="the-anweddol-project@proton.me",
    url="https://github.com/the-anweddol-project/Anweddol-client",
    description="The Anweddol client implementation",
    long_description=getReadmeContent(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Internet",
    ],
    license="MIT",
    packages=[
        "anwdlclient",  # Includes every CLI modules at the root of 'anwdlclient'
        "anwdlclient.core",
        "anwdlclient.tools",
        "anwdlclient.web",
    ],
    install_requires=["cryptography", "cerberus", "pyyaml", "requests"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "anwdlclient = anwdlclient.cli:MainAnweddolClientCLI",
        ],
    },
)
