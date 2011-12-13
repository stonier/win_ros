##############################################################################
# Overview
##############################################################################

# Detect ros environment variable settiings in the windows registry.

import os
import sys

##############################################################################
# Functions
##############################################################################

def detect_variable(name):
    var = os.getenv(name)
    print ("%s: %s"%(name, var))

##############################################################################
# Main
##############################################################################

def main():
    detect_variable("ROS_ROOT")
    detect_variable("ROS_MASTER_URI")
    detect_variable("ROS_PACKAGE_PATH")
    detect_variable("ROS_HOME")
    detect_variable("ROS_IP")
    detect_variable("PATH")
    detect_variable("PYTHONHOME")
    detect_variable("PYTHONPATH")
    os.system("pause")
    return 0

if __name__ == "__main__":
    sys.exit(main())
