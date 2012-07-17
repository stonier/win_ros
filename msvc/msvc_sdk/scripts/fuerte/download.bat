@echo off

rem rd /S /Q src

set PWD=%~dp0

if X%1==Xunstable (
  call rosinstall src https://raw.github.com/stonier/win_ros/master/msvc_unstable.rosinstall
) else (
  call rosinstall src https://raw.github.com/stonier/win_ros/master/msvc_fuerte.rosinstall
)
call src\setup.bat
cd src\win_ros\win_patches
call apply_msvc_patches
cd ..\msvc\msvc_sdk\scripts\fuerte
copy configure.bat %PWD%
copy *.cmake %PWD%
cd %PWD%

