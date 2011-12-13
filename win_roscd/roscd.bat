@echo off


REM TODO Should check for rospack here and emit a warning if unavailable 

if "%1"=="" (
	set pkgpath=%ROS_ROOT%
) else (
for /f %%i in ('rospack find %1') do set pkgpath=%%i
)

if NOT DEFINED pkgpath exit /b

set convertedpkgpath=%pkgpath:/=\%
cd /d %convertedpkgpath%
set pkgpath=
set convertedpkgpath=