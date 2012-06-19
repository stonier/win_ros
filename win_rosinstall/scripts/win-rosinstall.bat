ECHO OFF

REM Used to help execute win-rosinstall because windows is trivially fixated 
REM on extensions.

win-rosinstall.py --catkin %*
win-setupfiles.py %1