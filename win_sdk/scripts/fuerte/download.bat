echo OFF

REM rd /S /Q src
REM call win-rosinstall --catkin src msvc_catkin.rosinstall
call win-rosinstall --catkin src https://raw.github.com/stonier/win_ros/master/msvc_fuerte.rosinstall
call src\setup.bat
cd src\win_ros\win_patches
apply_msvc_patches
