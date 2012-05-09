@echo off
REM Should really clear rosdeps and redownload them too.

set PWD=%~dp0

echo "Clearing workspace"
rm -f %PWD%\download.bat
rm -f %PWD%\configure.bat
rm -f *.cmake
rm -rf C:\opt\ros\fuerte
rm -rf %PWD%\build
rm -rf %PWD%\src

echo "Rosinstalling, patching and build configuration"
wget --no-check-certificate https://raw.github.com/stonier/win_ros/master/win_sdk/scripts/fuerte/download.bat
call download
echo "Build - cmake"
REM call %PWD%\src\setup.bat
call configure
echo "Build - compile"
cd build
nmake
echo "Build - install"
nmake install

cd %PWD%