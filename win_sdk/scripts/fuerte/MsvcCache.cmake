get_filename_component(CWD ${CMAKE_CURRENT_LIST_FILE} PATH)

###########################
# WinRos
###########################
set(ROSDEPS_ROOT "C:/opt/rosdeps/x86" CACHE STRING "System root for many rosdep installations.")
set(INSTALL_ROOT "${CWD}/ros-sdk" CACHE PATH "Install root.")

###########################
# CMake
###########################
set(CMAKE_BUILD_TYPE RelWithDebInfo CACHE STRING "Build mode.")
set(CMAKE_INSTALL_PREFIX ${INSTALL_ROOT} CACHE PATH "Install root location.")
set(CMAKE_INCLUDE_PATH ${ROSDEPS_ROOT}/include CACHE STRING "Prefix to the system include directories.")
set(CMAKE_PREFIX_PATH ${ROSDEPS_ROOT} CACHE STRING "Prefix to the system directories.")

###########################
# Catkin
###########################
set(CATKIN_BLACKLIST_STACKS "None" CACHE STRING "Semi-colon separated list of stacks to exclude from the build.")
set(CATKIN_BUILD_PROJECTS "All" CACHE STRING "Semi-colon list of stacks to build.")

###########################
# Boost
###########################
set(Boost_DEBUG FALSE CACHE BOOL "Debug boost.")
set(Boost_DETAILED_FAILURE_MSG FALSE CACHE BOOL "Detailed failure reports from boost.")
# BOOST_ALL_NO_LIB : don't auto-link in windoze (better portability -> see FindBoost.cmake)
# BOOST_ALL_DYN_LINK=1 : actually redundant since we turn off auto-linking above
# Ordinarily it will choose dynamic links instead of static links

