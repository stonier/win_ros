@echo off

rem **************************** Variables ***********************************

set BUILD=stable
rem set BUILD=unstable
if "%BUILD%" == "stable" (
  set SDK_VERSION=0.1.2
) else (
  set SDK_VERSION=0.1.3
)
set INSTALL_ROOT=C:\opt
set SDK_INSTALL_PREFIX=%INSTALL_ROOT%\ros\fuerte\x86
set COMMS_INSTALL_PREFIX=%INSTALL_ROOT%\roscomms\fuerte\x86
rem alternatively put it directly in your sdk folder
rem set COMMS_INSTALL_PREFIX=%SDK_INSTALL_PREFIX%
set ROSDEPS_ROOT=%INSTALL_ROOT%\rosdeps\fuerte\x86

rem ***************************** Constants **********************************

set PWD=%~dp0
set DIR_SDK_SOURCES=%PWD%sdk
set DIR_COMMS_SOURCES=%PWD%comms
set DIR_SDK_BUILD=%PWD%build_sdk
set DIR_COMMS_BUILD=%PWD%build_comms
set DIR_PATCHES=%DIR_SDK_SOURCES%\win_ros\win_patches\patches
set DIR_SDK_FILES=%DIR_SDK_SOURCES%\win_ros\msvc\msvc_sdk\scripts\fuerte
set SDK_ZIP=sdk-fuerte-x86-vs10-%SDK_VERSION%.zip
set COMMS_ZIP=comms-fuerte-x86-vs10-%SDK_VERSION%.zip
set COMMAND=%1
set TARGET=%2

rem ************************** Options Parser ********************************

if X%COMMAND%==X set COMMAND=help
if X%COMMAND%==Xhelp goto Help
if X%COMMAND%==Xsdk goto Sdk
if X%COMMAND%==Xcomms goto Comms
goto Help

:Help
echo.
echo Usage: winros [subcommand] [target]
echo.
echo Various commands used to help build various targets for winros.
echo.
echo Type 'winros [subcommand] help' for more detailed usage.
echo.
echo   sdk        build/bundle the winros sdk
echo   comms      generate headers and modules for ros msgs/srvs.
echo.
goto End

:SdkHelp
echo.
echo Usage: winros sdk [target]
echo.
echo Various targets used for building the winros sdk.
echo.
echo If not building the 'all' target, make sure the others
echo are called in the correct sequence.
echo.
echo   clean      clean the workspace (remove build and source directories)
echo   all        download, configure, build and install
echo   download   rosinstall the winros sdk sources
echo   configure  run cmake on the sources
echo   build      compile sources and generate comms
echo   install    install everything to %INSTALL_ROOT%
echo   package    zip the installation (requires 7z)
echo   upload     upload the sdk to the server
echo.
goto End

:Sdk
if X%TARGET%==X set COMMAND=help
if X%TARGET%==Xhelp goto SdkHelp
if X%TARGET%==Xclean goto SdkClean
if X%TARGET%==Xall goto SdkDownload
if X%TARGET%==Xdownload goto SdkDownload
if X%TARGET%==Xcmake goto SdkConfigure
if X%TARGET%==Xconfigure goto SdkConfigure
if X%TARGET%==Xbuild goto SdkBuild
if X%TARGET%==Xinstall goto SdkInstall
if X%TARGET%==Xpackage goto SdkPackage
if X%TARGET%==Xupload goto SdkUpload
goto SdkHelp

:CommsHelp
echo.
echo Usage: winros comms [target]
echo.
echo Various targets used for building the winros sdk.
echo.
echo If not building the 'all' target, make sure the others
echo are called in the correct sequence.
echo.
echo   clean      clean the workspace (remove build and source directories)
echo   all        download, configure, build and install
echo   download   rosinstall minimal set of generators and comms stacks
echo   configure  run cmake on the comms stacks
echo   build      configure and generate cpp headers and python modules
echo   install    install everything to %INSTALL_ROOT%
echo   package    zip the installation (requires 7z)
echo   upload     upload the sdk to the server
echo.
goto End

:Comms
if X%TARGET%==X set COMMAND=help
if X%TARGET%==Xhelp goto CommsHelp
if X%TARGET%==Xclean goto CommsClean
if X%TARGET%==Xall goto CommsDownload
if X%TARGET%==Xdownload goto CommsDownload
if X%TARGET%==Xcmake goto CommsConfigure
if X%TARGET%==Xconfigure goto CommsConfigure
if X%TARGET%==Xbuild goto CommsBuild
if X%TARGET%==Xinstall goto CommsInstall
if X%TARGET%==Xpackage goto CommsPackage
if X%TARGET%==Xupload goto CommsUpload
goto CommsHelp


rem *************************** Sdk Targets **********************************

:SdkClean
echo.
echo "Cleaning workspace and installation"
echo.
@echo on
rm -rf %INSTALL_ROOT%\ros\fuerte
rm -rf %INSTALL_ROOT%\rosws\fuerte
rm -f %INSTALL_ROOT%\%SDK_ZIP%
rm -rf %DIR_SDK_BUILD%
rm -rf %DIR_SDK_SOURCES%
@echo off
goto End

:SdkDownload
echo.
if "%BUILD%"=="stable" (
  echo "Downloading stable sources."
  echo.
  call rosinstall %DIR_SDK_SOURCES% https://raw.github.com/stonier/win_ros/master/msvc_fuerte.rosinstall
) else (
  echo "Downloading latest sources."
  echo.
  call rosinstall %DIR_SDK_SOURCES% https://raw.github.com/stonier/win_ros/master/msvc_unstable.rosinstall
)
cd %DIR_SDK_SOURCES%\win_ros\win_patches
call apply_msvc_patches
cd %PWD%
if X%TARGET%==Xall (
  goto SdkConfigure
) else (
  echo.
  echo "You may now proceed with 'winros sdk configure'"
  goto End
)

:SdkConfigure
echo.
echo "Configuring the build"
echo.
call %DIR_SDK_SOURCES%\setup.bat
if not exist %DIR_SDK_BUILD% mkdir %DIR_SDK_BUILD%
cd %DIR_SDK_BUILD%
rem You can use a cache file for this, like
rem cmake -G "NMake Makefiles" -C "%DIR_SDK_FILES%\MsvcCache.cmake" -DCMAKE_USER_MAKE_RULES_OVERRIDE:STRING="%DIR_SDK_FILES%\MsvcFlags.cmake" %DIR_SDK_SOURCES%
rem
rem 1) CATKIN_BUILD_STACKS and BLACKLIST_STACKS are semicolon separated list of stack names (ALL and None are the defaults).
rem   e.g. -DCATKIN_BUILD_STACKS:STRING="catkin;genmsg;gencpp;ros;roscpp_core"
rem 2) Boost_xxx variables are useful for debugging boost problems.
rem
cmake -G "NMake Makefiles" ^
	  -DCMAKE_BUILD_TYPE=RelWithDebInfo ^
	  -DCMAKE_INSTALL_PREFIX:PATH=%SDK_INSTALL_PREFIX% ^
	  -DCATKIN_ROSDEPS_PATH:PATH=%ROSDEPS_ROOT% ^
	  -DCATKIN_BUILD_STACKS:STRING=ALL ^
	  -DCATKIN_BLACKLIST_STACKS:STRING=None ^
	  -DBoost_DEBUG:BOOL=False ^
	  -DBoost_DETAILED_FAILURE_MSG=False ^
	  -DCMAKE_USER_MAKE_RULES_OVERRIDE:STRING="%DIR_SDK_FILES%\MsvcFlags.cmake" ^
	  %DIR_SDK_SOURCES%
cd %PWD%
if X%TARGET%==Xall (
  goto SdkBuild
) else (
  echo.
  echo "You may now proceed with 'winros sdk build'"
  goto End
)

:SdkBuild
echo.
echo "Compiling sources and generating headers/modules"
echo.
cd %DIR_SDK_BUILD%
nmake
cd %PWD%
if X%TARGET%==Xall (
  goto SdkInstall
) else (
  echo.
  echo "You may now proceed with 'winros sdk install'"
  goto End
)

:SdkInstall
echo.
echo "Install the build packages and the sdk project tutorials"
cd %DIR_SDK_BUILD%
nmake install
cd ..
echo -- Installing %INSTALL_ROOT%\rosws\fuerte\sdk-tutorials
rm -rf %INSTALL_ROOT%\rosws\fuerte
mkdir %INSTALL_ROOT%\rosws\fuerte
cp -r %DIR_SDK_SOURCES%\win_ros\tutorials\msvc_sdk_tutorials %INSTALL_ROOT%\rosws\fuerte\sdk-tutorials
goto End

:SdkPackage
echo.
echo "Packaging the SDK"
echo.
cd %INSTALL_ROOT%
7z a -r %SDK_ZIP% ros rosdeps rosws
goto End

:SdkUpload
echo.
echo "Uploading to file server."
echo.
cd %INSTALL_ROOT%
scp %SDK_ZIP% files@files.yujinrobot.com:pub/win_ros/sdk
goto End

rem ************************** Comms Targets *********************************

:CommsClean
echo.
echo "Cleaning comms workspace"
echo.
@echo on
rm -rf %COMMS_INSTALL_PREFIX%
rm -rf %DIR_COMMS_BUILD%
rm -rf %DIR_COMMMS_SOURCES%
@echo off
goto End

:CommsDownload
echo.
if "%BUILD%"=="stable" (
  echo "Downloading stable generators and comms sources."
  echo.
  call rosinstall %DIR_COMMS_SOURCES% https://raw.github.com/stonier/win_ros/master/msvc_fuerte_comms.rosinstall
) else (
  echo "Downloading latest generators and comms sources."
  echo.
  call rosinstall %DIR_COMMS_SOURCES% https://raw.github.com/stonier/win_ros/master/msvc_unstable_comms.rosinstall
)
cd %PWD%
if X%TARGET%==Xall (
  goto SdkConfigure
) else (
  echo.
  echo "You may now proceed with 'winros comms configure'"
  goto End
)

:CommsConfigure
echo.
echo "Configuring the build"
echo.
call %DIR_COMMS_SOURCES%\setup.bat
if not exist %DIR_COMMS_BUILD% mkdir %DIR_COMMS_BUILD%
cd %DIR_COMMS_BUILD%
rem 1) CATKIN_BUILD_STACKS and BLACKLIST_STACKS are semicolon separated list of stack names (ALL and None are the defaults).
rem   e.g. -DCATKIN_BUILD_STACKS:STRING="catkin;genmsg;gencpp;genpy"
cmake -G "NMake Makefiles" ^
	  -DCATKIN_BUILD_STACKS:STRING=ALL ^
      -DCATKIN_BLACKLIST_STACKS:STRING="win_ros" ^
	  -DCMAKE_INSTALL_PREFIX=%COMMS_INSTALL_PREFIX% ^
	  %DIR_COMMS_SOURCES%
cd %PWD%
if X%TARGET%==Xall (
  goto CommsBuild
) else (
  echo.
  echo "You may now proceed with 'winros comms build'"
  goto End
)

:CommsBuild
echo.
echo "Generating headers and python modules"
echo.
cd %DIR_COMMS_BUILD%
nmake
cd %PWD%
if X%TARGET%==Xall (
  goto CommsInstall
) else (
  echo.
  echo "You may now proceed with 'winros comms install'"
  goto End
)

:CommsInstall
echo.
echo "Install headers and python modules to %COMMS_INSTALL_PREFIX%"
echo.
cd %DIR_COMMS_BUILD%
nmake install
cd %PWD%
goto End

:CommsPackage
echo.
echo "Packaging comms headers and python modules (requires 7z)"
echo.
cd %COMMS_INSTALL_PREFIX%
7z a -r %COMMS_ZIP% .
goto End

:End
cd %PWD%
