@echo off

set PWD=%~dp0
@set WORKSPACE=%cd%
@set SRC_DIR=%WORKSPACE%\src
@set BLD_DIR=%WORKSPACE%\build
set COMMAND=%1
set INSTALL_ROOT=C:\opt

if X%COMMAND%==X set COMMAND=all
if X%COMMAND%==Xhelp goto Help
if X%COMMAND%==Xclean goto Clean
if X%COMMAND%==Xall goto Clean
if X%COMMAND%==Xdownload goto Download
if X%COMMAND%==Xbuild goto Build
if X%COMMAND%==Xinstall goto Install
goto Help

:Help
echo "Usage: call with args from ['clean', 'all', 'download', 'build', 'install']"
goto End

:Clean
@echo on
echo.
echo "Cleaning the workspace"
IF EXIST %PWD%msvc_unstable_comms.rosinstall rm -f %PWD%msvc_unstable_comms.rosinstall
IF EXIST %PWD%build rm -rf %PWD%build
IF EXIST %PWD%src rm -rf %PWD%src
@echo off
if X%COMMAND%==Xall (
  goto Download
) else (
  goto End
)

:Download
echo.
echo "Rosinstalling, patching and cmake invocation"
cd %PWD%
IF EXIST %PWD%msvc_unstable_comms.rosinstall rm -f %PWD%msvc_unstable_comms.rosinstall
wget --no-check-certificate https://raw.github.com/stonier/win_ros/master/msvc_unstable_comms.rosinstall
call rosinstall %SRC_DIR% msvc_unstable_comms.rosinstall
if X%COMMAND%==Xall (
  goto Build
) else (
  goto End
)

:Build
echo.
cd %PWD%
echo %PWD%1240520
IF NOT EXIST %PWD%build mkdir build
cd build
echo "Configure"
cmake -G "NMake Makefiles" -DCATKIN_BLACKLIST_STACKS="win_ros" -DCMAKE_INSTALL_PREFIX=%INSTALL_ROOT%\ros_comms\fuerte\x86 %SRC_DIR%
echo "Build and install"
nmake
if X%COMMAND%==Xall (
  goto Install
) else (
  goto End
)

:Install
echo.
echo "Install the build packages and the sdk project tutorials"
cd %PWD%
cd build
nmake install
cd ..
echo -- Installing %INSTALL_ROOT%\rosws\fuerte\sdk-tutorials
rm -rf C:\opt\rosws\fuerte
mkdir C:\opt\rosws\fuerte
rem cp -r %PWD%\src\win_ros\tutorials\msvc_sdk_tutorials %INSTALL_ROOT%\rosws\fuerte\sdk-tutorials
goto End

:End
cd %PWD%
