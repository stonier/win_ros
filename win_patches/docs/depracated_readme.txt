
== std_msgs ==

  - remove unnecessary dependency on roslib in manifest.xml

== cpp_common ==

  - provide a generic macro for handling msvc import/export and gcc visibility
    - https://code.ros.org/trac/ros/attachment/ticket/3514
  - better msvc checking for stdint type definitions (vis studio 10 is ok).
  - added a centralised location for including windows.h
  - cross platform functions in platform.h

== rospy ==

  - add a python call to the genmsg_cpp add_custom_commands to work around a windows bug handling long arg strings
  
== rostime ==

 - Fixes
   - provide a generic macro for handling msvc import/export and gcc visibility
   - define NOMINMAX 
     - the C++ std library's min and max function templates are used, rather than MS's legacy min and max macros.
   - use boost for round function
   - inline non-template functions in impl/duration.h
   - removed windows.h calls to #include <ref/platform.h> in cpp_common because of careful macro sequencing before windows.h.
   
 - Warnings
   - pragmas to disable msvc not looking up the impl/* headers (how does gcc do this?)
   - delete the declaration of the throw in ros_walltime, not needed and gives warnings in msvc.
   - dont do uint64 arithmetic when we're calculating int64's in time.cpp.
 
== roscpp_serialization ==

 - provide a generic macro for handling msvc import/export and gcc visibility
 - comment pre-processor about stdint.h in types.h 
    - MSVC10 support stdint library

== XmlRpc == 
 - provide a generic macro for handling msvc import/export and gcc visibility
 - do not include strings.hpp in windows
 - non fatal error handling via WSA### macros instead of errno macros (XmlRpcSocket.cpp).
 - remove windoze depracated warnings for sprintf, snprintf sscanf, strerror by moving to the xxx_s variants on _MSC_VER.
 
== rosconsole ==

 - provide a generic macro for handling msvc import/export and gcc visibility
 - no varg_copy on windows, just hack by assignment.
 - windows log4cxx usually defaults to wchar type, not char type, must use ENCODE to convert to strings of char type.
 - remove windows warnings for depracated functions, use vnsprintf and getenv -> vnsprintf_s and _dupenv_s. 
 - dont actually need the target_link_libraries for the thirdparty dep log4cxx.
 - TODO : get log4cxx and rosconsole working together to handle multi-byte languages (e.g. korean)
 - removed windows.h calls to cpp_common's ros/platform.h

 == roscpp ==

 - see accompanying roscpp.txt
 
== roscpp_tutorials ==

 - fixing time_api so that it does ros::Time::init(), actually is this supposed to be automatically done under the hood?
 - temporarily including boost directories so ros/time.h can find boost headers.
 - temporarily adding log4cxx to the 3rdparty dependencies so it can find it too.
 
== roslib ==

 - added definition to avoid a warning thrown by msvc when using some boost (in rosbuild.cmake).
 - added export macros
 
== actionlib_msgs ==

 - path generation for action msg targets had a double slash (instead of a single), windows cmake couldn't recognise them, fixed.
 
== actionlib ==
 
 - export macros
 - temporarily adding log4cxx to the dependencies since it doesn't pass it down from rosconsole
 - exclude tests from ALL
 - fix the list iterator bug in managed_lists (see http://www.rhinocerus.net/forum/language-c-moderated/627695-assigning-value-unassigned-iterator.html) 
 
 