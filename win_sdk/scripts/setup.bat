echo OFF
REM
REM This script readies the environment for running ros
REM programs with the sdk.
REM 
REM - sets up paths so binaries can find ros and rosdep dlls
REM - configures important ros environment variables
REM
REM Modify them as appropriate for your environment.
REM

set PATH=%PATH%;%PROGRAMFILES%\boost\boost_1_44\lib
set PATH=%PATH%;C:\work\ros-sdk\debug\bin
set ROS_MASTER_URI=http://192.168.10.161:11311
set ROS_IP=192.168.10.67

