ECHO OFF

rem Used to help execute rosinstall because windows doesn't know
rem what to do if it doesn't have a .py extension.

set DIR=%~dp0
python %DIR%\win-rosinstall.py --catkin %*
python %DIR%\win-rosinstall-setupfiles.py %1