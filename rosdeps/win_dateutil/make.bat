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
IF NOT EXIST %cd%\build (
  echo.
  echo "Downloading sources and patching"
  echo.
  mkdir build
  cd build
  call wget http://labix.org/download/python-dateutil/python-dateutil-1.5.tar.gz
  call tar -xvzf python-dateutil-1.5.tar.gz
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
IF NOT EXIST %cd%\build\python-dateutil-1.5\dist (
  cd %cd%\build\python-dateutil-1.5
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
cd %cd%\build\python-dateutil-1.5\dist
scp *.msi files@files.yujinrobot.com:pub/windows/python/2.7/
goto End

:Clean
rd /S /Q %cd%\build
goto End

:End
cd %PWD%



