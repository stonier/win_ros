ECHO OFF

REM Used to help execute win-rosinstall because windows is trivially fixated 
REM on extensions.

REM Don't actually need PYTHONHOME defined if %PYTHONHOME%\Scripts is in the path
REM IF DEFINED PYTHONHOME (python %PYTHONHOME%\Scripts\rosinstall %*) ELSE (ECHO PYTHONHOME variable is not set, please rectify.)

win-rosinstall.py %*
