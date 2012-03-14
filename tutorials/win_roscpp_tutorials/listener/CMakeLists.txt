include_directories(${ROS_INCLUDE_DIRS})
add_executable(win_listener listener.cpp )
target_link_libraries(win_listener ${ROS_LIBRARIES}) 
install(TARGETS win_listener RUNTIME DESTINATION share/win_roscpp_tutorials/bin)

