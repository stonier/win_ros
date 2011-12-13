cmake_minimum_required(VERSION 2.4.6)
include($ENV{ROS_ROOT}/core/rosbuild/rosbuild.cmake)

rosbuild_init()

add_custom_target(
        populate_bin ALL
        cmake -E copy scripts/winshell.bat ../bin
        COMMAND cmake -E copy scripts/winclear.py ../bin
        COMMAND cmake -E copy scripts/windetect.py ../bin
        COMMAND cmake -E copy scripts/winsetup.py ../bin
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        COMMENT "Moving windows setup scripts to win_ros/bin."
        )
