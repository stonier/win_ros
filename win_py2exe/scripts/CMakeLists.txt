
add_custom_target(
  copy_into_ros_root_bin
  ALL
  COMMAND cmake -E copy rosmaster.bat ${CMAKE_BINARY_DIR}/bin   
  COMMAND cmake -E copy roscore.bat ${CMAKE_BINARY_DIR}/bin   
  COMMAND cmake -E copy rosversion.bat ${CMAKE_BINARY_DIR}/bin   
  COMMAND cmake -E copy roslaunch.bat ${CMAKE_BINARY_DIR}/bin   
  COMMAND cmake -E copy rostopic.bat ${CMAKE_BINARY_DIR}/bin   
  COMMAND cmake -E copy rosbag.bat ${CMAKE_BINARY_DIR}/bin   
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  COMMENT "Copying python enabling batch scripts to the ros bin dir."
  VERBATIM
)

install(FILES
  rosmaster.bat
  roscore.bat
  rosversion.bat
  roslaunch.bat
  rostopic.bat
  rosbag.bat
  DESTINATION bin
)

# Need an install files here.