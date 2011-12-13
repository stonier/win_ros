ECHO OFF

REM Used to help execute rosinstall because windows is trivially fixated 
REM on extensions.

IF DEFINED PYTHONHOME (python %PYTHONHOME%\Scripts\winrosinstall.py %*) ELSE (ECHO PYTHONHOME variable is not set, please rectify.)