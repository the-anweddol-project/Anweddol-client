"""
    Copyright 2023 The Anweddol project
    See the LICENSE file for licensing informations
    ---

    Client installation script

"""
from setuptools import setup
import getpass
import os

anweddol_base_path = (
    f"C:\\Users\\{getpass.getuser()}\\Anweddol\\"
    if os.name == "nt"
    else f"/home/{getpass.getuser()}/.anweddol/"
)
local_ifs = "\\" if os.name == "nt" else "/"

print("Creating base folder ...")
if not os.path.exists(anweddol_base_path):
    os.mkdir(anweddol_base_path)

print("Creating configuration file ...")
if os.path.exists(anweddol_base_path + "config.yaml"):
    os.remove(anweddol_base_path + "config.yaml")

# Replace arbitrary values in the resource config file before copy it on the system
with open(
    f"{os.path.dirname(os.path.realpath(__file__))}{local_ifs}resources{local_ifs}config.yaml",
    "r",
) as fd:
    data = (
        fd.read()
        .replace(
            "session_credentials_path",
            anweddol_base_path + f"credentials{local_ifs}session_credentials.db",
        )
        .replace(
            "container_credentials_path",
            anweddol_base_path + f"credentials{local_ifs}container_credentials.db",
        )
        .replace(
            "access_token_path",
            anweddol_base_path + f"credentials{local_ifs}access_token.db",
        )
        .replace("rsa_keys_path", anweddol_base_path + f"rsa_keys{local_ifs}")
    )

    with open(anweddol_base_path + "config.yaml", "w") as fd:
        fd.write(data)

print("Installing Anweddol client ...")
setup(
    name="anwdlclient",
    version="1.0.0",
    description="The Anweddol client implementation",
    author="The Anweddol project",
    author_email="the-anweddol-project@proton.me",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Topic :: Internet",
        "Topic :: System :: Emulators",
    ],
    license="GPL v3",
    url="https://github.com/the-anweddol-project/Anweddol-client",
    packages=["anwdlclient"],
    install_requires=["cryptography", "cerberus", "pyyaml"],
    include_package_data=True,
    entry_points={
        "console_scripts": ["anwdlclient = anwdlclient.cli:MainAnweddolClientCLI"],
    },
)
