
@REM We are assuming that all source stacks are two directories below this and nowhere else.
@set DIR=%~dp0
@set PATCH_DIR=%DIR%patches
@set ROOT_DIR=%DIR%..\..

@echo "PATCHING"
@echo ""
@echo "  Dir..........%DIR%"
@echo "  Patch Dir....%PATCH_DIR%"
@echo "  Source Dir...%ROOT_DIR%"
@echo ""

cd %ROOT_DIR%
@for /f %%a in ('dir /b %PATCH_DIR%\*.patch') do patch -p0 < %PATCH_DIR%\%%a

@REM xcopy %cd%\updates\* %ROS_ROOT%\..\ /E /Y /EXCLUDE:exclude_svn.txt
@cd %DIR%
