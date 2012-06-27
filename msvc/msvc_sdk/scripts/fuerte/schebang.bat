@echo off
rem This is a superbuilder script that downloads, compiles and
rem packages and uploads the winros sdk.
rem
rem Prerequisites:
rem 
rem - rosdeps are already installed
rem - required python modules are already installed

set SDK_VERSION=0.1.1
set INSTALL_ROOT=C:\opt
set SDK_ZIP=sdk-fuerte-x86-vx10-%SDK_VERSION%.zip
set PWD=%~dp0
set COMMAND=%1

if X%COMMAND%==X set COMMAND=all
if X%COMMAND%==Xhelp goto Help
if X%COMMAND%==Xclean goto Clean
if X%COMMAND%==Xall goto Clean
if X%COMMAND%==Xdownload goto Download
if X%COMMAND%==Xbuild goto Build
if X%COMMAND%==Xinstall goto Install
if X%COMMAND%==Xpackage goto Package
if X%COMMAND%==Xupload goto Upload
goto Help

:Help
echo "Usage: call with args from ['clean', 'all', 'download', 'build', 'install', 'package', 'upload']"
goto End

:Clean
echo.
echo "Cleaning the workspace"
rm -f %PWD%\download.bat
rm -f %PWD%\configure.bat
rm -f *.cmake
rm -rf %INSTALL_ROOT%\ros\fuerte
rm -rf %INSTALL_ROOT%\rosws\fuerte
rm -f %INSTALL_ROOT%\sdk-fuerte-x86-vx10-%SDK_VERSION%.zip
rm -rf %PWD%\build
rm -rf %PWD%\src
if X%COMMAND%==Xall (
  goto Download
) else (
  goto End
)

:Download
echo.
echo "Rosinstalling, patching and cmake invocation"
cd %PWD%
wget --no-check-certificate https://raw.github.com/stonier/win_ros/master/msvc/msvc_sdk/scripts/fuerte/download.bat
call download
REM call %PWD%\src\setup.bat
call configure
if X%COMMAND%==Xall (
  goto Build
) else (
  goto End
)

:Build
echo.
echo "Build and install"
cd %PWD%
cd build
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
rm -rf C:\opt\rosws\fuerte
mkdir C:\opt\rosws\fuerte
cp -r %PWD%\src\win_ros\msvc\msvc_sdk\sdk_projects\fuerte\sdk-tutorials C:\opt\rosws\fuerte\sdk-tutorials
if X%COMMAND%==Xall (
  goto Package
) else (
  goto End
)

:Package
echo.
echo "Packaging the SDK"
cd %INSTALL_ROOT%
7z a -r %SDK_ZIP% ros rosdeps rosws
if X%COMMAND%==Xall (
  goto Upload
) else (
  goto End
)

:Upload
echo "Uploading to file server."
cd %INSTALL_ROOT%
scp %SDK_ZIP% files@files.yujinrobot.com:pub/win_ros/sdk
goto End

:End
cd %PWD%
