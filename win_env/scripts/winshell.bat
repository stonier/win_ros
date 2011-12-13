@echo OFF

echo Setting environment for RoS.

set ROS_INSTALL_ROOT=C:\Users\rosbuild\hudson\work
set ROS_ROOT=%ROS_INSTALL_ROOT%\ros
set PYTHONHOME=C:\Python27
set PYTHONPATH=%ROS_ROOT%\core\roslib\src
set PATH=%PATH%;%ROS_INSTALL_ROOT%\ros\bin;%ROS_INSTALL_ROOT%\win_ros\bin;%PYTHONHOME%;%PYTHONHOME%\Scripts

set ROS_PACKAGE_PATH=%ROS_INSTALL_ROOT%\ros_comm;%ROS_INSTALL_ROOT%\ros_tutorials;%ROS_INSTALL_ROOT%\win_ros;
set ROS_MASTER_URI=http://localhost:11311

doskey wordpad="C:\Program Files\Windows NT\Accessories\wordpad.exe" $1
doskey roscd=%ROS_INSTALL_ROOT%\win_ros\win_roscd\roscd.bat $1

REM
REM ********************* Rosbuild2 **********************
REM
REM Relevant only if using rosbuild2 (not the mingw environment).
REM Search paths for dlls, this is just a hack for now
set PATH=%PATH%;C:/opt/3rdparty/lib;C:/opt/3rdparty/bin;C:/Program Files/boost/boost_1_44/lib;C:/work/rosbuild2/build/lib;

REM If you want to start a shell directly from this batch file, uncomment one of the following.
REM cmd
REM Note, if using the default generator (nmake), collect the visual studio shell settings
REM cmd /k "C:\Program Files\Microsoft Visual Studio 10.0\VC\vcvarsall.bat" x86
REM cmd /k "C:\Program Files\Microsoft Visual Studio 9.0\VC\vcvarsall.bat" x86

REM Otherwise, set this batch file with a /k in the shortcut starting a shell promopt. 
REM Don't forgot to include vs settings if using the nmake generator
REM On 32 bit systems
REM "C:\Program Files\Microsoft Visual Studio 10.0\VC\vcvarsall.bat"
REM On 64 bit systems
"C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\vcvarsall.bat"

