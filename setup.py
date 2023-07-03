"""
    Copyright 2023 The Anweddol project
    See the LICENSE file for licensing informations
    ---

    Client installation script

"""
from subprocess import Popen, PIPE
from setuptools import setup
import getpass
import shutil
import os

ACTUAL_VERSION = "1.1.2"


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

print("[SETUP] Creating uninstallation script ...")
if os.name == "nt":
    shutil.copyfile(
        os.path.dirname(os.path.realpath(__file__))
        + f"{local_ifs}resources{local_ifs}anwdlclient-uninstall.bat",
        anweddol_base_path + "anwdlclient-uninstall.bat",
    )

else:
    shutil.copyfile(
        os.path.dirname(os.path.realpath(__file__))
        + f"{local_ifs}resources{local_ifs}anwdlclient-uninstall",
        f"/home/{getpass.getuser()}/.local/bin/anwdlclient-uninstall",
    )
    executeCommand(
        f"chmod +x /home/{getpass.getuser()}/.local/bin/anwdlclient-uninstall"
    )

print("[SETUP] Installing Anweddol client ...")
setup(
    name="anwdlclient",
    version=ACTUAL_VERSION,
    author="The Anweddol project",
    author_email="the-anweddol-project@proton.me",
    url="https://github.com/the-anweddol-project/Anweddol-client",
    description="The Anweddol client implementation",
    long_description=getReadmeContent(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Topic :: Internet",
        "Topic :: System :: Emulators",
    ],
    license="GPL v3",
    packages=["anwdlclient", "anwdlclient.core", "anwdlclient.tools"],
    install_requires=["cryptography", "cerberus", "pyyaml"],
    include_package_data=True,
    entry_points={
        "console_scripts": ["anwdlclient = anwdlclient.cli:MainAnweddolClientCLI"],
    },
)
