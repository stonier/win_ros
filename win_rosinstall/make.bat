ECHO OFF
REM
REM Make sure you have bumped the version in setup.py and scripts/winrosinstall.py before doing this.
REM

IF X%1==Xclean GOTO Clean
IF X%1==Xdistro GOTO Distro
IF X%1==Xall GOTO Compile
IF X%1==Xcompile GOTO Compile

ECHO "Invalid usage: call with args from ['clean', 'all', 'distro']"
GOTO End

:Compile
IF NOT EXIST %cd%\src\vcstools (
  REM This is tip 02/03/2012
  hg clone -r 3dec7e9f442d https://kforge.ros.org/vcstools/hg vcstools
  hg clone -r 59a772e5cddc https://kforge.ros.org/vcstools/rosinstall rosinstall
  move %cd%\vcstools\src\vcstools %cd%\src\vcstools
  move %cd%\rosinstall\src\rosinstall %cd%\src\rosinstall
  rd /S /Q vcstools
  rd /S /Q rosinstall
  copy %cd%\patches\svn.py %cd%\src\vcstools
)
IF X%1==Xall GOTO Distro

:Clean
rd /S /Q %cd%\build
rd /S /Q %cd%\dist
rd /S /Q %cd%\src\vcstools
rd /S /Q %cd%\src\rosinstall
GOTO End

:Distro
python setup.py bdist_wininst
GOTO End

:End