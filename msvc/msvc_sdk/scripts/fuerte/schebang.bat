@echo off
REM Should really clear rosdeps and redownload them too.

set PWD=%~dp0

echo "Clearing workspace"
rm -f %PWD%\download.bat
rm -f %PWD%\configure.bat
rm -f *.cmake
rm -rf C:\opt\ros\fuerte
rm -rf C:\opt\ros\fuerte
rm -rf C:\opt\projects
rm -rf %PWD%\build
rm -rf %PWD%\src

echo "Rosinstalling, patching and build configuration"
wget --no-check-certificate https://raw.github.com/stonier/win_ros/master/msvc/msvc_sdk/scripts/fuerte/download.bat
call download
echo "Build - cmake"
REM call %PWD%\src\setup.bat
call configure

echo "Build - compile"
cd build
nmake

echo "Build - install"
nmake install

echo "Downloading Projects"
mkdir C:\opt\projects
cd C:\opt\projects
wget http://files.yujinrobot.com/win_ros/sdk-tutorials-fuerte-x86-vs10.zip
7z x sdk-tutorials-fuerte-x86-vs10.zip
rm sdk-tutorials-fuerte-x86-vs10.zip

echo "Bundling SDK"

cd %PWD%
