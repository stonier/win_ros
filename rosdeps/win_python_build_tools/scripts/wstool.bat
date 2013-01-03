ECHO OFF

REM Used to help execute wstool because windows is trivially fixated 
REM on extensions.

set DIR=%~dp0
python %DIR%\win-wstool.py %*
REM python %DIR%\win-wstool-setupfiles.py %1