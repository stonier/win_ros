set HUDSON=C:\Users\rosbuild\hudson
set ROSWIN=%HUDSON%\workspace\roswin
mkdir %ROSWIN%

copy %cd%\..\win_sdk\scripts\schebang.bat %ROSWIN%
copy %cd%\resources\hudson.bat %HUDSON%
copy %cd%resources\slave.jar %HUDSON%
