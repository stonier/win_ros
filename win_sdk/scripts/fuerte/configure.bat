echo OFF

REM ******** Configurable Variables ******

set ROSDEPS_ROOT="C:\opt\rosdeps\x86"
set CATKIN_BUILD_PROJECTS=ALL
set CMAKE_BUILD_TYPE=RelWithDebInfo
set BOOST_ROOT="C:\Program Files (x86)\boost\boost_1_44"

REM ************** Variables *************

set WORKSPACE=%cd%
set SRC_DIR=%WORKSPACE%\src
set BLD_DIR=%WORKSPACE%\build
set SDK_DIR=%WORKSPACE%\ros-sdk
set SDK_DBG_DIR=%WORKSPACE%\ros-sdk\debug
set SDK_REL_DIR=%WORKSPACE%\ros-sdk\release

if X%1==Xclean goto Clean
if X%1==Xall goto All

REM Default option 
GOTO All

REM *****************************************************
:All

REM ********** Directories **********
rd /S /Q %BLD_DIR%
mkdir %BLD_DIR%
cd %BLD_DIR%

REM ************* Cmake *************
echo ON
REM -DBoost_INCLUDE_DIR=%ROSDEPS_ROOT% ^
REM -D CATKIN_BLACKLIST_STACKS=%CATKIN_BUILD_PROJECTS% ^
REM -D Log4cxx_DIR:PATH=%ROSDEPS_ROOT%/share/cmake/log4cxx ^

cmake -G "NMake Makefiles" ^
-D CMAKE_BUILD_TYPE:PATH=%CMAKE_BUILD_TYPE% ^
-D CMAKE_INSTALL_PREFIX:PATH=%SDK_DBG_DIR% ^
-D CMAKE_INCLUDE_PATH:PATH=%BOOST_ROOT% ^
-D CMAKE_PREFIX_PATH:PATH=%ROSDEPS_ROOT% ^
-D BOOST_ROOT:PATH=%BOOST_ROOT% ^
%SRC_DIR%

echo OFF
cd ..
GOTO End

REM *****************************************************
:Clean

rd /S /Q %BLD_DIR%
GOTO End

REM *****************************************************
 
:End
