cmake_minimum_required(VERSION 2.4.6)
include($ENV{ROS_ROOT}/core/rosbuild/rosbuild.cmake)

rosbuild_init()

add_custom_target(
        populate_bin ALL
        cmake -E copy roscd.bat ../bin
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        COMMENT "Moving roscd.bat to win_ros/bin."
        )
