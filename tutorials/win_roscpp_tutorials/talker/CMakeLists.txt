include_directories(${ROS_INCLUDE_DIRS})
add_executable(win_talker talker.cpp)
target_link_libraries(win_talker ${ROS_LIBRARIES}) 
install(TARGETS win_talker RUNTIME DESTINATION share/win_roscpp_tutorials/bin)


  
