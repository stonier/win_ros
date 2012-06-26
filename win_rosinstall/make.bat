@ECHO OFF

IF X%1==Xclean GOTO Clean
IF X%1==Xdistro GOTO Compile
IF X%1==Xall GOTO Compile
IF X%1==Xcompile GOTO Compile
IF X%1==Xupload GOTO Compile
IF X%1==Xversion GOTO Version

ECHO "Invalid usage: call with args from ['clean', 'all', 'distro', 'upload', 'version']"
GOTO End

: Version
echo.
echo "Make sure you bump the version in setup.py if necessary."
GOTO End

:Compile
IF NOT EXIST %cd%\scripts\win-rosinstall.py (
  REM This is tip 02/03/2012
  hg clone -r 15d0b6e38e2e https://kforge.ros.org/vcstools/hg vcstools
  hg clone -r 4ab7a92fdf07 https://kforge.ros.org/vcstools/rosinstall rosinstall
  move %cd%\vcstools\src\vcstools %cd%\src\vcstools
  move %cd%\rosinstall\src\rosinstall %cd%\src\rosinstall
  move %cd%\rosinstall\scripts\rosinstall %cd%\scripts\win-rosinstall.py
  rd /S /Q vcstools
  rd /S /Q rosinstall
  REM copy /Y %cd%\patches\svn.py %cd%\src\vcstools
  REM copy /Y %cd%\patches\multiproject_cmd.py %cd%\src\rosinstall
) ELSE (
  echo.
  echo "Already prepped"
)
IF X%1==Xdistro GOTO Distro
IF X%1==Xall GOTO Distro
IF X%1==Xupload GOTO Distro
GOTO End

:Distro
REM python setup.py bdist_wininst
IF NOT EXIST %cd%\dist (
  python setup.py bdist_msi
) ELSE (
  echo.
  echo "Msi installer already built"
)
IF X%1==Xupload GOTO Upload
IF X%1==Xall GOTO Upload

:Upload
cd dist
scp *.msi files@files.yujinrobot.com:pub/appupdater/python/2.7/
GOTO End


:Clean
rd /S /Q %cd%\build
rd /S /Q %cd%\dist
rd /S /Q %cd%\src\vcstools
rd /S /Q %cd%\src\rosinstall
rm %cd%\scripts\win-rosinstall.py
GOTO End


GOTO End

:End