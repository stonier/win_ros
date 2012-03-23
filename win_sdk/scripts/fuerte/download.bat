echo OFF

REM rd /S /Q src
REM call win-rosinstall --catkin src https://raw.github.com/stonier/win_ros/master/msvc_fuerte.rosinstall
REM call src\setup.bat
cd src\win_ros\win_patches
REM apply_msvc_patches
cd ..\win_sdk\scripts\fuerte
copy *.bat C:\work
copy *.cmake C:\work
