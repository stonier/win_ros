get_filename_component(CWD ${CMAKE_CURRENT_LIST_FILE} PATH)

###########################
# WinRos
###########################
set(ROSDEPS_ROOT "C:/opt/rosdeps/x86" CACHE STRING "System root for many rosdep installations.")
set(INSTALL_ROOT "${CWD}/ros-sdk" CACHE PATH "Install root.")

###########################
# CMake
###########################
# If you change the build type, make sure you change the argument (/Debug, /Release) used when 
# calling the msvc sdk/visual studio environment script
set(CMAKE_BUILD_TYPE RelWithDebInfo CACHE STRING "Build mode.")
set(CMAKE_INSTALL_PREFIX ${INSTALL_ROOT} CACHE PATH "Install root location.")
set(CATKIN_ROSDEPS_PATH ${ROSDEPS_ROOT} CACHE STRING "Prefix to the rosdep root directory(s).")

###########################
# Catkin
###########################
set(CATKIN_BLACKLIST_STACKS "None" CACHE STRING "Semi-colon separated list of stacks to exclude from the build.")
set(CATKIN_BUILD_PROJECTS "All" CACHE STRING "Semi-colon list of stacks to build.")
#set(CATKIN_BUILD_PROJECTS "catkin;roscpp_core" CACHE STRING "Semi-colon list of stacks to build.")

###########################
# Boost
###########################
set(Boost_DEBUG FALSE CACHE BOOL "Debug boost.")
set(Boost_DETAILED_FAILURE_MSG FALSE CACHE BOOL "Detailed failure reports from boost.")

