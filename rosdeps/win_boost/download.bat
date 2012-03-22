echo OFF

git clone --branch=cmake-1.47.0 git://gitorious.org/boost/cmake.git boost
cp patches/* boost/tools/build/CMake/install_me/