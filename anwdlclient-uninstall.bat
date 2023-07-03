@echo off

REM Simple script that uninstalls the Anweddol client on Windows

echo.Deleting system files ...
rmdir C:\\Users\%USERNAME%\\Anweddol

echo.Uninstalling 'anwdlclient' package ...
py -m pip uninstall anwdlclient -y