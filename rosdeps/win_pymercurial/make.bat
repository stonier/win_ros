echo off

REM This needs to be done on a system with ms express or ms visual studio
REM Windows sdk7.1 just won't do (it is wanting vcvarsall.bat). Example call:
REM 
REM Environment settings for your compiler [MS Express]
REM "call C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\vcvarsall.bat"
REM 
mkdir build
cd build
wget http://mercurial.selenic.com/release/mercurial-2.1.1.tar.gz
tar -xvzf mercurial-2.1.1.tar.gz
cd mercurial-2.1.1
setup.py bdist_msi
cd ..

