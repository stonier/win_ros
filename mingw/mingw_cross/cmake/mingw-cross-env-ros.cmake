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
# Qt
###############################

set(QT_IS_STATIC 1) # Works on my gentoo (cmake 2.8.1), fails on lucid ubuntu (cmake 2.8.0)
set(QT_QMAKE_EXECUTABLE ${TOOLCHAIN_TUPLE}-qmake CACHE PATH "Qmake location") 

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
#MARK_AS_ADVANCED(CMAKE_GENERATOR CMAKE_FIND_ROOT_PATH CMAKE_TOOLCHAIN_FILE TOOLCHAIN_FAMILY TOOLCHAIN_TUPLE TOOLCHAIN_SYSROOT)

