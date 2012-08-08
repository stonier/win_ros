###############################################################################
# Family : mingw_cross
# Tuple : i686-pc-mingw32
# Sysroot : $(MINGW_ROOT)/usr/i686-pc-mingw32
# CMake Toolchain File: ${SYSROOT}/share/cmake/mingw-cross-env-conf.cmake
###############################################################################

set(TOOLCHAIN_TUPLE i686-pc-mingw32)

###############################
# Boost
###############################

# Boost needs to be hand held on windoze for boost_thread.
# Maybe bad place for this? Could also embed in rosbuild/public.cmake
# WIN_32_WINNT : needed to find symbols properly
#   refer to http://lists-archives.org/mingw-users/04689-linking-help.html
# BOOST_THREAD_USE_LIB : needed to tell it to cleanup properly 
#   refer to http://lists.gnu.org/archive/html/mingw-cross-env-list/2011-05/msg00060.html
set(MINGW_CROSS_COMPILE_FLAGS "-DBOOST_THREAD_USE_LIB -D_WIN32_WINNT=0x0501")
set(Boost_THREADAPI "win32" CACHE STRING "Necessary variable for cmake to find mingw boost, needs cmake v2.8.3+")
#set(Boost_USE_STATIC_LIBS TRUE CACHE STRING "Using static libs for boost.")

set(CMAKE_C_FLAGS ${MINGW_CROSS_COMPILE_FLAGS} CACHE PATH "Compile flags for c.")
set(CMAKE_CXX_FLAGS ${MINGW_CROSS_COMPILE_FLAGS} CACHE PATH "Compile flags for c++.")

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
set(QT_IS_STATIC true CACHE BOOL "Qt will use static libraries") # Works on my gentoo (cmake 2.8.1), fails on lucid ubuntu (cmake 2.8.0)
set(QT_QMAKE_EXECUTABLE ${TOOLCHAIN_TUPLE}-qmake CACHE STRING "The qmake executable")

###############################
# SSE
###############################
# No way of knowing if the target machine has sse, so lets disable by default
# so ros doesn't fall over on the TRY_RUN tests.
# The user can always renable them in his cache config file.
set(HAS_SSE_EXTENSIONS_EXITCODE FALSE CACHE BOOL "Cross-compiling variable en/disabling sse extensions.")
set(HAS_SSE2_EXTENSIONS_EXITCODE FALSE CACHE BOOL "Cross-compiling variable en/disabling sse2 extensions.")
set(HAS_SSE3_EXTENSIONS_EXITCODE FALSE CACHE BOOL "Cross-compiling variable en/disabling sse3 extensions.")



