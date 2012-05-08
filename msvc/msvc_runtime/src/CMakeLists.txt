###############################################################################
# Files
###############################################################################

#set(ROS_BIN_DIR ${CMAKE_BINARY_DIR}/bin)

#configure_file(${CMAKE_CURRENT_SOURCE_DIR}/ros_bin.cpp.in
#    ${CMAKE_CURRENT_SOURCE_DIR}/ros_bin.cpp
#    )

macro(add_pyexe name)
  # make the target name unique so we don't clash (e.g. rosbag target)
  add_executable(${name}_exe ros_bin.cpp)
  install(TARGETS ${name}_exe RUNTIME DESTINATION bin)
  # ensure the output name isn't mucked up by the unique target name.
  set_target_properties(${name}_exe PROPERTIES OUTPUT_NAME ${name})
endmacro()

add_pyexe(rosmaster)
add_pyexe(roscore)
add_pyexe(rostopic)
add_pyexe(roslaunch)
#add_pyexe(rosbag) # Not ported yet
add_pyexe(rosparam)
add_pyexe(rosversion)
add_pyexe(rosservice)
#add_pyexe(rosrun) # It's a bash file, not a python file
add_pyexe(roswtf)

