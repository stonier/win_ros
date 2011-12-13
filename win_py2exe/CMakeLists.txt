cmake_minimum_required(VERSION 2.4.6)
include($ENV{ROS_ROOT}/core/rosbuild/rosbuild.cmake)

# Set the build type.  Options are:
#  Coverage       : w/ debug symbols, w/o optimization, w/ code-coverage
#  Debug          : w/ debug symbols, w/o optimization
#  Release        : w/o debug symbols, w/ optimization
#  RelWithDebInfo : w/ debug symbols, w/ optimization
#  MinSizeRel     : w/o debug symbols, w/ optimization, stripped binaries
#set(ROS_BUILD_TYPE RelWithDebInfo)

rosbuild_init()

#set the default path for built executables to the "bin" directory
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)

add_subdirectory(src)

if(WIN32)
  set(ROSXXX_EXE rosxxx.exe)
  set(ROSXXX_PATHNAME ${CMAKE_SOURCE_DIR}/bin/${ROSXXX_EXE})
  add_custom_target(
    copy_into_ros_root_bin
    ALL
    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/rosversion.exe   
    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/rosmaster.exe   
    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/rostopic.exe   
    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/rosservice.exe   
    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/roscore.exe   
    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/roslaunch.exe
    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/roscreate-pkg.exe
    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/roscreate-stack.exe
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Copying files."
    VERBATIM
  )
  add_dependencies(copy_into_ros_root_bin rosxxx)
else()
  message(WARNING "This package is only useful when compiling for windows.")
endif()

 