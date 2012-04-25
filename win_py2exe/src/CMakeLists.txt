###############################################################################
# Files
###############################################################################

set(ROS_BIN_DIR ${CMAKE_BINARY_DIR}/bin)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/ros_bin.cpp.in
    ${CMAKE_CURRENT_SOURCE_DIR}/ros_bin.cpp
    )

macro(add_pyexe name)
  add_executable(${name} ros_bin.cpp)
  install(TARGETS ${name} RUNTIME DESTINATION bin)
endmacro()

add_pyexe(rosmaster)
# Not working yet (python issues)
add_pyexe(roscore)
add_pyexe(rostopic)
add_pyexe(roslaunch)
add_pyexe(rosbag)
add_pyexe(rosversion)
#add_pyexe(rosservice)
#add_pyexe(rosrun)
#add_pyexe(roswtf)
