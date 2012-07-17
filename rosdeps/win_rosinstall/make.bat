@ECHO OFF

set PWD=%~dp0
set COMMAND=%1
if X%COMMAND%==X set COMMAND=all
if X%COMMAND%==Xhelp goto Help
if X%COMMAND%==Xclean goto Clean
if X%COMMAND%==Xall goto Download
if X%COMMAND%==Xdownload goto Download
if X%COMMAND%==Xdistro goto Distro
if X%COMMAND%==Xupload goto Upload
goto Help

:Help
echo.
echo "Invalid usage: call with args from ['clean', 'all', 'download', 'distro', 'upload']"
echo "Make sure you bump the version in setup.py if necessary."
goto End

:Download
IF NOT EXIST %cd%\scripts\win-rosinstall.py (
  echo.
  echo "Downloading sources and patching"
  echo.
  REM This is tip 02/03/2012
  call hg clone -r 15d0b6e38e2e https://kforge.ros.org/vcstools/hg vcstools
  call hg clone -r 4ab7a92fdf07 https://kforge.ros.org/vcstools/rosinstall rosinstall
  move %cd%\vcstools\src\vcstools %cd%\src\vcstools
  move %cd%\rosinstall\src\rosinstall %cd%\src\rosinstall
  move %cd%\rosinstall\scripts\rosinstall %cd%\scripts\win-rosinstall.py
  rd /S /Q vcstools
  rd /S /Q rosinstall
  rem put patching here if we want it
) ELSE (
  echo.
  echo "Already prepped"
)
if X%COMMAND%==Xall (
  goto Distro
) else (
  goto End
)

:Distro
echo.
echo "Building msi installer."
echo.
IF NOT EXIST %cd%\dist (
  python setup.py bdist_msi
) ELSE (
  echo.
  echo "Msi installer already built"
)
if X%COMMAND%==Xall (
  goto Upload
) else (
  goto End
)

:Upload
echo.
echo "Uploading to file server."
echo.
cd dist
scp *.msi files@files.yujinrobot.com:pub/appupdater/python/2.7/
goto End

:Clean
rd /S /Q %cd%\build
rd /S /Q %cd%\dist
rd /S /Q %cd%\src\vcstools
rd /S /Q %cd%\src\rosinstall
rm %cd%\scripts\win-rosinstall.py
goto End

:End
cd %PWD%