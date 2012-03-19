
mkdir build
cd build
wget http://www.alcyone.com/software/empy/empy-latest.tar.gz
tar -xvzf empy-latest.tar.gz
cd empy-3.3
setup.py bdist_msi
cd ..
