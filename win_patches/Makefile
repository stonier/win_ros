# Trailing slash indicates do not copy the folder
FROM:=`pwd`/updates/
DEST:=${ROS_ROOT}/..

OPTIONS=--recursive
EXCLUDES=--exclude '.svn'

help:
	@echo "Nothing to see here"

# This is the old rsync I was using to update with patches.
# Now use either apply_mingw_patches or update.bat

all:
	rsync ${OPTIONS} ${EXCLUDES} ${FROM} ${DEST}

CPP_COMMON=ros_comm/utilities/cpp_common

cpp_common:
	rsync ${OPTIONS} ${EXCLUDES} ${FROM}${CPP_COMMON}/ ${DEST}/${CPP_COMMON}


ROSTIME=ros_comm/utilities/rostime

rostime: cpp_common
	rsync ${OPTIONS} ${EXCLUDES} ${FROM}${ROSTIME}/ ${DEST}/${ROSTIME}


XMLRPCPP=ros_comm/utilities/xmlrpcpp

xmlrpcpp: 
	rsync ${OPTIONS} ${EXCLUDES} ${FROM}${XMLRPCPP}/ ${DEST}/${XMLRPCPP}


STD_MSGS=ros_comm/messages/std_msgs

std_msgs:
	rsync ${OPTIONS} ${EXCLUDES} ${FROM}${STD_MSGS}/ ${DEST}/${STD_MSGS}

ROSCONSOLE=ros_comm/tools/rosconsole

rosconsole: rostime 
	rsync ${OPTIONS} ${EXCLUDES} ${FROM}${ROSCONSOLE}/ ${DEST}/${ROSCONSOLE}

SERIALIZATION=ros_comm/clients/cpp/roscpp_serialization

roscpp_serialization: rostime 
	rsync ${OPTIONS} ${EXCLUDES} ${FROM}${SERIALIZATION}/ ${DEST}/${SERIALIZATION}

ROSCPP=ros_comm/clients/cpp/roscpp

roscpp: roscpp_serialization xmlrpcpp rosconsole std_msgs
	rsync ${OPTIONS} ${EXCLUDES} ${FROM}${ROSCPP}/ ${DEST}/${ROSCPP}

ROSPY=ros_comm/clients/rospy

rospy:
	rsync ${OPTIONS} ${EXCLUDES} ${FROM}${ROSPY}/ ${DEST}/${ROSPY}



