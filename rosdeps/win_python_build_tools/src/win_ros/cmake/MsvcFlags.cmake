# Only way I can find to set global compiler flags.
#
# BOOST_ALL_NO_LIB : don't auto-link in windoze (better portability -> see FindBoost.cmake)
# BOOST_ALL_DYN_LINK=1 : actually redundant since we turn off auto-linking above
# Ordinarily it will choose dynamic links instead of static links
set(CMAKE_CXX_FLAGS_INIT "${CMAKE_CXX_FLAGS_INIT} /DBOOST_ALL_NO_LIB /DBOOST_ALL_DYN_LINK")
