REM echo OFF
REM
REM This script does the hudson test run by default.
REM It should also leave the installation ready to be packaged.
REM
REM You'll need the vcs tools (svn, git, mercurial) and build tools
REM (cmake, wget, ms visual studio) before running this script.
REM 

REM ************ Build Options ************

REM set SOURCE_TYPE=unstable
set SOURCE_TYPE=stable

REM ************* Directories *************

set WORKSPACE=%CD%
set SRC_DIR=%WORKSPACE%\src
set BLD_DIR=%WORKSPACE%\build
set BLD_DBG_DIR=%BLD_DIR%\debug
set BLD_REL_DIR=%BLD_DIR%\release
set SDK_DIR=%WORKSPACE%\ros-sdk
set SDK_DBG_DIR=%WORKSPACE%\ros-sdk\debug
set SDK_REL_DIR=%WORKSPACE%\ros-sdk\release

set PYTHONHOME=C:\Python27
set PYTHON=%PYTHONHOME%\python

REM **************** Clean ****************

rd /S /Q %SRC_DIR%
rd /S /Q %BLD_DIR%
rd /S /Q %SDK_DIR%
mkdir %BLD_DBG_DIR%
mkdir %BLD_REL_DIR%
mkdir %SDK_DBG_DIR%
mkdir %SDK_REL_DIR%

REM *************** 3rdparty **************

REM Just downloading the appropriate one into the sdk directory for now.
cd %SDK_DIR%
wget http://win-ros-pkg.googlecode.com/files/log4cxx-x86-vs10.tar.gz
tar -xvzf log4cxx-x86-vs10.tar.gz
rm log4cxx-x86-vs10.tar.gz
rm debug\log4cxx.txt
rm release\log4cxx.txt
cd %WORKSPACE%

REM *************** Sources ***************

IF "%SOURCE_TYPE%" == "unstable" (
    REM *************** We need the delete-changed-uris because git is hopeless with ***************
    call rosinstall %SRC_DIR% "http://packages.ros.org/cgi-bin/gen_rosinstall.py?rosdistro=electric&variant=robot&overlay=no"
    call rosinstall %SRC_DIR% "http://win-ros-pkg.googlecode.com/svn/stacks/win_ros/trunk/win_hudson/resources/msvc_electric_hudson.rosinstall" --delete-changed-uris
) ELSE (
    call rosinstall %SRC_DIR% "http://win-ros-pkg.googlecode.com/svn/stacks/win_ros/trunk/msvc_electric.rosinstall" --delete-changed-uris
)

call %SRC_DIR%\setup.bat

REM ************ Apply patches ************

cd %SRC_DIR%\win_ros\win_patches
call update

REM *************** Debug *****************

cd %BLD_DBG_DIR%
cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=%SDK_DBG_DIR% -DLOG4CXX_ROOT_DIR=%SDK_DBG_DIR% %SRC_DIR%
CALL :NMake
CALL :NMakeInstall

REM *************** Release ***************

cd %BLD_REL_DIR%
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%SDK_REL_DIR% -DLOG4CXX_ROOT_DIR=%SDK_REL_DIR% %SRC_DIR%
CALL :NMake
CALL :NMakeInstall

REM ************ Sdk Tutorial *************

mkdir %SDK_DIR%\sdk_tutorials
xcopy %SRC_DIR%\win_ros\win_sdk\sdk_tutorials %SDK_DIR%\sdk_tutorials /E /Y /EXCLUDE:%SRC_DIR%\win_ros\win_patches\exclude_svn.txt
copy %SRC_DIR%\win_ros\win_sdk\scripts\setup.bat %SDK_DIR%
GOTO End

REM ************* Subroutines *************

:NMake
  cd roscpp_tutorials
  nmake
  cd ..\actionlib
  nmake
  cd ..\std_msgs
  nmake
  cd ..\nav_msgs
  nmake
  cd ..\geometry_msgs
  nmake
  cd ..
GOTO :EOF

:NMakeInstall
  cd cpp_common
  nmake install
  cd ..\rostime
  nmake install
  cd ..\roslib
  nmake install
  cd ..\roscpp_serialization
  nmake install
  cd ..\xmlrpcpp
  nmake install
  cd ..\rospack
  nmake install
  cd ..\rosconsole
  nmake install
  cd ..\roscpp_traits
  nmake install
  cd ..\roscpp
  nmake install
  cd ..\roscpp_tutorials
  nmake install
  cd ..\rosgraph_msgs
  nmake install
  cd ..\std_msgs
  nmake install
  cd ..\nav_msgs
  nmake install
  cd ..\geometry_msgs
  nmake install
  cd ..
GOTO :EOF

:End