#!/bin/bash

# Simple script that uninstalls the Anweddol client on linux-based systems

echo "Deleting system files ..."
rm -rf ~/.anweddol

echo "Uninstalling 'anwdlclient' package ... "
pip uninstall anwdlclient -y