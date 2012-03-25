echo OFF

REM ************** Variables *************

set WORKSPACE=%cd%
set SRC_DIR=%WORKSPACE%\src
set BLD_DIR=%WORKSPACE%\build

if X%1==Xclean goto Clean

REM Default option 

REM ********** Directories **********
rd /S /Q %BLD_DIR%
mkdir %BLD_DIR%
cd %BLD_DIR%

REM ************* Cmake *************
echo ON

cmake -G "NMake Makefiles" -C "%WORKSPACE%\MsvcCache.cmake" -DCMAKE_USER_MAKE_RULES_OVERRIDE:STRING="%WORKSPACE%\MsvcFlags.cmake" %SRC_DIR%

echo OFF
cd ..
GOTO End

REM *****************************************************
:Clean

rd /S /Q %BLD_DIR%
GOTO End

REM *****************************************************
 
:End
