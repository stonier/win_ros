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
echo "Usage: call with args from ['clean', 'all', 'download', 'distro']"
goto End

:Download
IF NOT EXIST %cd%\rospkg (
  echo.
  echo "Downloading and patching code."
  call git clone https://github.com/ros/rospkg.git
  copy scripts\rosversion.bat rospkg\scripts\rosversion.bat
  rem Add rosversion.bat to the list of scripts to install
  sed -e s:rosversion"'":rosversion"'","'"scripts/rosversion.bat"'":g rospkg/setup.py > setup.py.tmp
  copy /Y setup.py.tmp rospkg\setup.py
  rm setup.py.tmp
) ELSE (
  echo.
  echo "Already cloned the rospkg repository."
)
if X%COMMAND%==Xall (
  goto Distro
) else (
  goto End
)

:Distro
echo.
echo "Building msi installer."
cd rospkg
python setup.py bdist_msi
cd ..
if X%COMMAND%==Xall (
  goto Upload
) else (
  goto End
)

:Upload
echo.
echo "Uploading to file server."
cd rospkg/dist
scp *.msi files@files.yujinrobot.com:pub/appupdater/python/2.7/
cd ..\..
goto End

:Clean
rd /S /Q %cd%\rospkg
goto End

:End
cd %PWD%