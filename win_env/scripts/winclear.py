##############################################################################
# Overview
##############################################################################
#
# Clears away the currently configured ros environment variables from the
# user's registry. Note that this completely blows away PATH and PYTHONPATH.
#
##############################################################################
# Imports
##############################################################################

import os
import sys
import _winreg

##############################################################################
# Functions
##############################################################################

def clear_variable(sub_key,name):
    try:
        _winreg.DeleteValue(sub_key,name)
        print "  - %s cleared"%name
    except:
        print "  - %s not found"%name

##############################################################################
# Main
##############################################################################

def main():
    ####################
    # Registry
    ####################
    root_key = _winreg.ConnectRegistry(None,_winreg.HKEY_CURRENT_USER)
    sub_key = _winreg.CreateKey(root_key,"Environment")
    print ""
    print "Clearing environment variables from the current user's registry:"
    print ""
    clear_variable(sub_key, "ROS_ROOT")
    clear_variable(sub_key, "ROS_MASTER_URI")
    clear_variable(sub_key, "ROS_HOME")
    clear_variable(sub_key, "ROS_IP")
    clear_variable(sub_key, "ROS_PACKAGE_PATH")
    clear_variable(sub_key, "PATH")
    clear_variable(sub_key, "PYTHONHOME")
    clear_variable(sub_key, "PYTHONPATH")

    ####################
    # Broadcasting
    ####################
    try:
        import win32gui
        import win32con
        win32gui.SendMessageTimeout(win32con.HWND_BROADCAST,win32con.WM_SETTINGCHANGE, 0,"Environment", 0, 1000 )
    except:
        print "Note that registry env variable changes aren't picked up by programs unless you log off, log on"
        print "                                                   OR"
        print "you have installed pywin32 so that this script can broadcast the change."
        print ""
        print "To install pywin32, download the appropraite file from:"
        print "     http://sourceforge.net/projects/pywin32/files/pywin32/"
        print ""

    os.system("pause")
    return 0

if __name__ == "__main__":
    sys.exit(main())

