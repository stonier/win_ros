ECHO OFF

REM Used to help execute rosws because windows is trivially fixated 
REM on extensions.

set DIR=%~dp0
python %DIR%\win-rosws.py %*
