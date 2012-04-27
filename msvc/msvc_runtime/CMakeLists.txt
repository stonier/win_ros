cmake_minimum_required(VERSION 2.8)
project(msvc_runtime)
find_package(ROS COMPONENTS catkin)
catkin_project(msvc_runtime)

include_directories(${ROS_INCLUDE_DIRS})

# We want to generate exe's calling the python scripts in the root bin folder.
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

if(WIN32)
  add_subdirectory(src)
  #add_subdirectory(scripts)  
else()
  message(WARNING "This package is only useful when compiling for windows.")
endif()
