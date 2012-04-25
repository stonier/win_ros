cmake_minimum_required(VERSION 2.8)
project(win_py2exe)
find_package(ROS COMPONENTS catkin)
catkin_project(win_py2exe)

include_directories(${ROS_INCLUDE_DIRS})

# We want to generate exe's calling the python scripts in the root bin folder.
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

if(WIN32)
  add_subdirectory(src)
  
#  set(ROSXXX_EXE rosxxx.exe)
#  set(ROSXXX_PATHNAME ${CMAKE_SOURCE_DIR}/bin/${ROSXXX_EXE})
#  add_custom_target(
#    copy_into_ros_root_bin
#    ALL
#    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/rosversion.exe   
#    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/rosmaster.exe   
#    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/rostopic.exe   
#    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/rosservice.exe   
#    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/roscore.exe   
#    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/roslaunch.exe
#    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/roscreate-pkg.exe
#    COMMAND cmake -E copy ${ROSXXX_PATHNAME} $ENV{ROS_ROOT}/bin/roscreate-stack.exe
#    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
#    COMMENT "Copying files."
#    VERBATIM
#  )
#  add_dependencies(copy_into_ros_root_bin rosxxx)
else()
  message(WARNING "This package is only useful when compiling for windows.")
endif()

 