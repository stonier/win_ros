##############################################################################
# Overview
##############################################################################

# Sets up environment variables permanently in the user's windows
# registry.

##############################################################################
# Modules
##############################################################################

import os
import sys
import _winreg

##############################################################################
# User Defined Variables
##############################################################################

ros_install_root=r"C:\work\winmaster"
ros_root=ros_install_root+r"\ros"
# for location of your logs (default is C:\Documents and Settings\%USERNAME%\.ros
ros_home = None
# for remote connections, set this to the remote http url.
ros_master_uri=r"http://localhost:11311"
# for remote connections, set this to your local ip, e.g 192.168.10.67
ros_ip = None
python_home=(r"C:\Python27;")
python_scripts=(r"C:\Python27\Scripts;")
user_pythonpath = ""
# This sets the user path, the system path will be added to it.
# Note that it deletes everything and replaces with ros paths
# only, we may need to modify this to catch the existing path, 
# and cache that to disk somewhere.

pythonpath=(
            ros_install_root+r"\ros\core\roslib\src;"+user_pythonpath
)

path=(ros_install_root+r"\win_ros\win_env\bin;"+
           ros_install_root+r"\win_ros\win_env\scripts;"+
           ros_install_root+r"\ros\bin;"+
           python_home +
           python_scripts
      )

ros_package_path=(
                  ros_install_root+r"\ros_comm;"+
                  ros_install_root+r"\ros_tutorials;"+
                  ros_install_root+r"\win_ros"
)

##############################################################################
# Functions
##############################################################################

def write_variable(sub_key,name,value):
    if value is not None:
        print "  %s: %s"%(name,value)
        _winreg.SetValueEx(sub_key,name,0,_winreg.REG_SZ,value)
    
##############################################################################
# Main
##############################################################################

def main():
    ####################
    # Registry
    ####################
    root_key = _winreg.ConnectRegistry(None,_winreg.HKEY_CURRENT_USER)
    sub_key = _winreg.CreateKey(root_key,"Environment")

    print "***** Setting environment variables in the user registry *****"
    print ""
    print "  Warning: this will overwrite existing user defined:"
    print ""
    print "    - PATH"
    print "    - PYTHONHOME"
    print "    - PYTHONPATH"
    print ""
    print "  Adding to registry:"
    print ""
    print ("Our list of variables so the user can see:")
    print ("ROS_INSTALL_PATH : %s"%ros_install_root)
    print ("ROS_MASTER_URI : %s"%ros_master_uri)
    print ("ROS_ROOT : %s"%ros_root)
    print ("ROS_HOME : %s"%ros_home)
    print ("ROS_IP : %s"%ros_ip)
    print ("PATH : %s"%path)
    print ("PYTHONHOME : %s"%python_home)
    print ("PYTHONPATH : %s"%pythonpath)
    print ""
                
    #prompt for Y/N
    answer = raw_input("\ncheck these and if you want to continue, enter Y : ")
    if ( answer != "y" and answer != "Y"):
        print ("The setting process is cancelled.")
        os.system("pause")
    else:
        write_variable(sub_key,"ROS_ROOT",ros_root)
        write_variable(sub_key,"ROS_MASTER_URI",ros_master_uri)
        write_variable(sub_key,"ROS_PACKAGE_PATH", ros_package_path)
        write_variable(sub_key,"PATH",path)
        write_variable(sub_key,"PYTHONHOME",python_home)
        write_variable(sub_key,"PYTHONPATH",pythonpath)
        write_variable(sub_key,"ROS_IP",ros_ip)
        write_variable(sub_key,"ROS_HOME", ros_home)
    
        _winreg.CloseKey(sub_key)
        _winreg.CloseKey(root_key)
    
        print ""
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


