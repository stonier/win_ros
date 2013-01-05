@ECHO OFF

IF X%1==Xclean GOTO Clean
IF X%1==Xcompile GOTO Compile
IF X%1==Xupload GOTO Upload
IF X%1==Xall GOTO Compile

ECHO "Invalid usage: call with args from ['clean', 'compile', 'upload', 'all']"
GOTO End

:Compile
IF NOT EXIST %cd%\fakeroot (
  set CMAKE_INSTALL_PREFIX=%cd%/fakeroot
  mkdir build
  mkdir fakeroot
  cd build
  cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX=%CMAKE_INSTALL_PREFIX% ..
  nmake
  nmake install
  cd ..
  cd fakeroot
  7z a -r bzip2-1.0.6-x86-vc10.zip *
  cd ..
) ELSE (
  echo.
  echo "Already built"
)
IF X%1==Xall GOTO Upload
GOTO End

:Upload
scp fakeroot/bzip2*.zip files@files.yujinrobot.com:pub/windows/repo/libraries 
GOTO End

:Clean
rd /S /Q %cd%\bin
rd /S /Q %cd%\lib
rd /S /Q %cd%\build
rd /S /Q %cd%\fakeroot
GOTO End

:End
