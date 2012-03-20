echo off

IF X%1==Xhelp GOTO Help
IF X%1==Xcompiled GOTO Compiled
IF X%1==Xclean GOTO Clean

echo "Building pure python module."
rd /S /Q %cd%\build
mkdir build
cd build
wget http://mercurial.selenic.com/release/mercurial-2.1.1.tar.gz
tar -xvzf mercurial-2.1.1.tar.gz
cd mercurial-2.1.1
setup.py --pure build_py -c -d . build_ext -i build_mo --force
setup.py --pure bdist_msi
cd ..
GOTO End

:Compiled 
echo "Building binaries - make sure your express/studio environment is set."
rd /S /Q %cd%\build
mkdir build
cd build
wget http://mercurial.selenic.com/release/mercurial-2.1.1.tar.gz
tar -xvzf mercurial-2.1.1.tar.gz
cd mercurial-2.1.1
setup.py bdist_msi
cd ..
GOTO End

:Help
echo "Valid targets:"
echo "  make          : builds the pure python module."
echo "  make compiled : builds compiled binaries."
echo "  make clean    : cleans the build directory."
echo "  make help"    : this help."
GOTO End

:Clean
rd /S /Q %cd%\build
GOTO End
 
:End