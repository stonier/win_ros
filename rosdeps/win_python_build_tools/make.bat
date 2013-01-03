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
  mkdir src
  rem vcstools 0.1.26 rosinstall 0.6.22 wstool 0.0.2, rospkg 1.0.17
  call git clone https://github.com/ros/rospkg.git
  cd rospkg & call git checkout 85310f77b412bb52a3190bcbadf3c0677be9ced4 & cd ..
  call git clone https://github.com/vcstools/vcstools.git
  cd vcstools & call git checkout c57f0ab7be2eede0ead237a783d2cf2c7dd94cba & cd ..  
  call git clone https://github.com/vcstools/rosinstall.git
  cd rosinstall & call git checkout 73451bff3dac0d45a79a5dc177ea7a8fd743da3e & cd ..
  call git clone https://github.com/vcstools/wstool.git
  cd wstool & call git checkout e2e4c03f915926ef45e142ea7c97df43fe1bf017 & cd ..
  move %cd%\vcstools\src\vcstools %cd%\src\vcstools
  move %cd%\rosinstall\src\rosinstall %cd%\src\rosinstall
  move %cd%\wstool\src\wstool %cd%\src\wstool
  move %cd%\wstool\scripts\wstool %cd%\scripts\win-wstool.py
  move %cd%\rospkg\src\rospkg %cd%\src\rospkg
  move %cd%\rospkg\scripts\rosversion %cd%\scripts\win-rosversion.py
  rem put patching here if we want it
  rem copy /Y %cd%\patches\common.py %cd%\src\rosinstall
  rem copy /Y %cd%\patches\multiproject_cli.py %cd%\src\rosinstall
  rem copy /Y %cd%\patches\config_elements.py %cd%\src\rosinstall
  rd /S /Q vcstools
  rd /S /Q rosinstall
  rd /S /Q wstool
  rd /S /Q rospkg
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
scp *.msi files@files.yujinrobot.com:pub/windows/python/2.7/
goto End

:Clean
rd /S /Q %cd%\build
rd /S /Q %cd%\dist
rd /S /Q %cd%\src\vcstools
rd /S /Q %cd%\src\rosinstall
rd /S /Q %cd%\src\wstool
rd /S /Q %cd%\src\rospkg
rm %cd%\scripts\win-wstool.py
rm %cd%\scripts\win-rosversion.py
goto End

:End
cd %PWD%