###############################################################################
# Family : mingw_cross
# Tuple : i686-pc-mingw32
# Sysroot : $(MINGW_ROOT)/usr/i686-pc-mingw32
###############################################################################

# Note that the MINGW_ROOT environment variable should be set and 
# $ENV{MINGW_ROOT}/usr/bin should be in your PATH to use this cmake 
# module (these will be set if you used ros to install mingw_cross).

# Some useful custom variables that uniquely define this toolchain module
set(TOOLCHAIN_FAMILY "mingw_cross")
set(TOOLCHAIN_TUPLE "i686-pc-mingw32" CACHE STRING "Toolchain signature identifying cpu-vendor-platform-clibrary.")
set(TOOLCHAIN_SYSROOT "$ENV{MINGW_ROOT}/usr/${TOOLCHAIN_TUPLE}" CACHE STRING "Root of the target development environment (libraries, headers etc).")
set(TOOLCHAIN_INSTALL_PREFIX "${TOOLCHAIN_SYSROOT}" CACHE STRING "Preferred install location when using the toolchain.")
# Boost needs to be hand held on windoze for boost_thread.
# Maybe bad place for this? Could also embed in rosbuild/public.cmake
# WIN_32_WINNT : needed to find symbols properly
#   refer to http://lists-archives.org/mingw-users/04689-linking-help.html
# BOOST_THREAD_USE_LIB : needed to tell it to cleanup properly 
#   refer to http://lists.gnu.org/archive/html/mingw-cross-env-list/2011-05/msg00060.html
set(TOOLCHAIN_COMPILE_FLAGS "-DBOOST_THREAD_USE_LIB -D_WIN32_WINNT=0x0501")
set(Boost_THREADAPI "win32" CACHE STRING "Necessary variable for cmake to find mingw boost, needs cmake v2.8.3+")
#set(Boost_USE_STATIC_LIBS TRUE CACHE STRING "Using static libs for boost.")

# Now the cmake variables
set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_C_COMPILER   ${TOOLCHAIN_TUPLE}-gcc) # Make sure these are in your PATH
set(CMAKE_CXX_COMPILER ${TOOLCHAIN_TUPLE}-g++)
set(CMAKE_RC_COMPILER ${TOOLCHAIN_TUPLE}-windres)
set(CMAKE_FIND_ROOT_PATH ${TOOLCHAIN_SYSROOT} CACHE STRING "Cmake search variable for finding libraries/headers.")
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER CACHE STRING "Whether to search for programs in the system root path")
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY CACHE STRING "Whether to search for libraries in the system root path")
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY CACHE STRING "Whether to search for headers in the system root path")
set(CMAKE_INSTALL_PREFIX ${TOOLCHAIN_INSTALL_PREFIX} CACHE PATH "Installation path")
set(CMAKE_C_FLAGS ${TOOLCHAIN_COMPILE_FLAGS} CACHE PATH "Compile flags for c.")
set(CMAKE_CXX_FLAGS ${TOOLCHAIN_COMPILE_FLAGS} CACHE PATH "Compile flags for c++.")

###############################
# Mingw Ecosystem is Static
###############################
set(ROS_BUILD_STATIC_EXES true CACHE BOOL "Build static executables")
set(ROS_BUILD_SHARED_EXES false CACHE BOOL "Build shared executables")
set(ROS_BUILD_STATIC_LIBS true CACHE BOOL "Build static libraries")
set(ROS_BUILD_SHARED_LIBS false CACHE BOOL "Build shared libraries")

set(BUILD_STATIC true CACHE BOOL "Build statically linked binaries")
set(BUILD_SHARED false CACHE BOOL "Build dynamically linked binaries")


###############################
# Prepare Qt Environment
###############################
set(QT_IS_STATIC 1) # Works on my gentoo (cmake 2.8.1), fails on lucid ubuntu (cmake 2.8.0)
set(QT_QMAKE_EXECUTABLE ${TOOLCHAIN_TUPLE}-qmake) 

###############################
# SSE
###############################
# No way of knowing if the target machine has sse, so lets disable by default
# so ros doesn't fall over on the TRY_RUN tests.
# The user can always renable them in his cache config file.
set(HAS_SSE_EXTENSIONS_EXITCODE FALSE CACHE BOOL "Cross-compiling variable en/disabling sse extensions.")
set(HAS_SSE2_EXTENSIONS_EXITCODE FALSE CACHE BOOL "Cross-compiling variable en/disabling sse2 extensions.")
set(HAS_SSE3_EXTENSIONS_EXITCODE FALSE CACHE BOOL "Cross-compiling variable en/disabling sse3 extensions.")

# Hide from cache's front page
MARK_AS_ADVANCED(CMAKE_GENERATOR CMAKE_FIND_ROOT_PATH CMAKE_TOOLCHAIN_FILE TOOLCHAIN_FAMILY TOOLCHAIN_TUPLE TOOLCHAIN_SYSROOT)

