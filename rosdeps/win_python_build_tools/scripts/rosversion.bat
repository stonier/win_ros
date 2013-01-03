@echo off

rem Used to help execute rosversion because windows is trivially fixated 
rem on extensions.

set DIR=%~dp0
python %DIR%\win-rosversion.py %*
