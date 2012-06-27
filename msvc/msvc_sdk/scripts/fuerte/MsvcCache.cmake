get_filename_component(CWD ${CMAKE_CURRENT_LIST_FILE} PATH)

###########################
# WinRos
###########################
set(ROSDEPS_ROOT "C:/opt/rosdeps/fuerte/x86" CACHE STRING "System root for ros dependency.")
set(INSTALL_ROOT "C:/opt/ros/fuerte/x86" CACHE PATH "Install root.")

###########################
# CMake
###########################
# Be careful changing the build type - the rosdeps are typically 
# built Release or RelWithDebInfo. Mixed mode building typically does
# not work with msvc, so Debug won't work against rosdeps built as stated
# above. 
# If you do want to build Debug:
# - compile the rosdeps in debug mode
# - call the visual studio shell script (usually in src/setup.bat) in debug mode
# - make sure any projects on top are built in debug mode also. 
set(CMAKE_BUILD_TYPE RelWithDebInfo CACHE STRING "Build mode.")
set(CMAKE_INSTALL_PREFIX ${INSTALL_ROOT} CACHE PATH "Install root location.")
set(CATKIN_ROSDEPS_PATH ${ROSDEPS_ROOT} CACHE STRING "Prefix to the rosdep root directory(s).")

###########################
# Catkin
###########################
# If you want to do a very minimal test (useful for quick catkin testing)
#set(CATKIN_BUILD_STACKS "catkin;genmsg;gencpp;ros;roscpp_core" CACHE STRING "Semi-colon list of stacks to build.")
set(CATKIN_BUILD_STACKS "ALL" CACHE STRING "Semi-colon list of stacks to build.")
set(CATKIN_BLACKLIST_STACKS "None" CACHE STRING "Semi-colon separated list of stacks to exclude from the build.")

###########################
# Boost
###########################
set(Boost_DEBUG FALSE CACHE BOOL "Debug boost.")
set(Boost_DETAILED_FAILURE_MSG FALSE CACHE BOOL "Detailed failure reports from boost.")

