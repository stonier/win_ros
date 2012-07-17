@echo off

rem rd /S /Q src

set PWD=%~dp0
@set WORKSPACE=%cd%
@set SRC_DIR=%WORKSPACE%\src
@set BLD_DIR=%WORKSPACE%\build

call win-rosinstall %SRC_DIR% msvc_unstable_comms.rosinstall
rem I don't think we need this
rem call src\setup.bat

@REM ********** Directories **********
@rd /S /Q %BLD_DIR%
@mkdir %BLD_DIR%
@cd %BLD_DIR%

@REM ************* Cmake *************

@rem Some comments:
@rem 
@rem   To change build mode, configure CMAKE_BUILD_TYPE in MsvcCache.cmake or add -DCMAKE_BUILD_TYPE=... here.
@rem
@rem   When choosing your generator, make sure you call the appropriate vcsvarall.bat script
@rem   before running this script.

rem not sure how much we need of msvccache and msvcflags (redundant?)
rem cmake -G "NMake Makefiles" -C "%WORKSPACE%\MsvcCache.cmake" %SRC_DIR%

cmake -G "NMake Makefiles" -DCATKIN_BLACKLIST_STACKS="win_ros" -DCMAKE_INSTALL_PREFIX=C:\opt\ros_comms\fuerte\x86 %SRC_DIR%

cd %PWD%

cd %BLD_DIR%