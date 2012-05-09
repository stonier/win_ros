@REM ************** Variables *************

@set WORKSPACE=%cd%
@set SRC_DIR=%WORKSPACE%\src
@set BLD_DIR=%WORKSPACE%\build

@if X%1==Xclean goto Clean

@REM ********** Directories **********
@rd /S /Q %BLD_DIR%
@mkdir %BLD_DIR%
@cd %BLD_DIR%

@REM ************* Cmake *************

@REM To change build mode, configure CMAKE_BUILD_TYPE in MsvcCache.cmake or add -DCMAKE_BUILD_TYPE=... here.
cmake -G "NMake Makefiles" -C "%WORKSPACE%\MsvcCache.cmake" -DCMAKE_USER_MAKE_RULES_OVERRIDE:STRING="%WORKSPACE%\MsvcFlags.cmake" %SRC_DIR%
@cd ..
@GOTO End

@REM *****************************************************
:Clean

@rd /S /Q %BLD_DIR%
@goto End

@REM *****************************************************
 
:End
