
mkdir build
cd build
wget http://pyyaml.org/download/pyyaml/PyYAML-3.10.tar.gz
tar -xvzf PyYAML-3.10.tar.gz
cd PyYAML-3.10
setup.py bdist_msi
cd ..
