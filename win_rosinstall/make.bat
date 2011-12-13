REM
REM Make sure you have bumped the version in setup.py and scripts/winrosinstall.py before doing this.
REM

IF EXIST %cd%\src\rosinstall\vcs GOTO Setup

svn checkout -r 15023 https://code.ros.org/svn/ros/stacks/ros_release/trunk/vcstools/src/vcstools src\rosinstall\vcs
copy %cd%\patches\git.py %cd%\src\rosinstall\vcs

:Setup
python setup.py bdist_wininst
