#!/usr/bin/env python

"""
usage: rosinstall [OPTIONS] INSTALL_PATH [ROSINSTALL FILES OR DIRECTORIES]
see: http://www.ros.org/wiki/win_rosinstall

Type 'win-rosinstall --help' for usage.

Common invocations:

initial checkout:   win-rosinstall ~/ros "http://packages.ros.org/cgi-bin/gen_rosinstall.py?rosdistro=diamondback&variant=ros-full&overlay=no"
subsequent update:  win-rosinstall ~/ros

"""
from __future__ import print_function
import os

import sys
from optparse import OptionParser
import yaml
import shutil
import rosinstall.multiproject_cmd
import rosinstall.rosinstall_cmd

from rosinstall.helpers import ROSInstallException, __ROSINSTALL_FILENAME
from rosinstall.common import MultiProjectException
import rosinstall.config
import win_rosinstall

def usage():
  print(__doc__ % vars())
  exit(1)

def rosinstall_main(argv):
  if len(argv) < 2:
    usage()
  args = argv[1:]
  parser = OptionParser(usage="usage: rosinstall [OPTIONS] INSTALL_PATH [ROSINSTALL FILES OR DIRECTORIES]\n\n\
rosinstall does the following:\n\
  1. Merges all URIs into new or existing .rosinstall file at PATH\n\
  2. Checks out or updates all version controlled URIs\n\
  3. If ros stack is installed from source, calls rosmake after checkout or updates.\n\
  4. Generates/overwrites updated setup files\n\n\
If running with --catkin mode:\
  1. Merges all URIs into new or existing .rosinstall file at PATH\n\
  2. Checks out or updates all version controlled URIs\n\
  4. Generates/overwrites updated setup files and creates CMakeLists.txt at the root.\n\n\
URIs can be web urls to remote .rosinstall files, local .rosinstall files,\n\
git, svn, bzr, hg URIs, or other (local directories)\n\
Later URIs will shadow packages of earlier URIs.\n",
                        epilog="See: http://www.ros.org/wiki/rosinstall for details\n")
  parser.add_option("-c", "--catkin", dest="catkin", default=False,
                    help="Declare this is a catkin build.",
                    action="store_true")
  parser.add_option("--cmake-prefix-path", dest="catkinpp", default=None,
                    help="Where to set the CMAKE_PREFIX_PATH, implies --catkin",
                    action="store")
  parser.add_option("--version", dest="version", default=False,
                    help="display version information",
                    action="store_true")
  parser.add_option("-n", "--nobuild", dest="nobuild", default=False,
                    help="skip the build step for the ROS stack",
                    action="store_true")
  parser.add_option("--rosdep-yes", dest="rosdep_yes", default=False,
                    help="Pass through --rosdep-yes to rosmake",
                    action="store_true")
  parser.add_option("--continue-on-error", dest="robust", default=False,
                    help="Continue despite checkout errors",
                    action="store_true")
  parser.add_option("--delete-changed-uris", dest="delete_changed", default=False,
                    help="Delete the local copy of a directory before changing uri.",
                    action="store_true")
  parser.add_option("--abort-changed-uris", dest="abort_changed", default=False,
                    help="Abort if changed uri detected",
                    action="store_true")
  parser.add_option("--backup-changed-uris", dest="backup_changed", default='',
                    help="backup the local copy of a directory before changing uri to this directory.",
                    action="store")
  parser.add_option("--diff", dest="vcs_diff", default=False,
                    help="shows a combined diff over all SCM entries",
                    action="store_true")
  parser.add_option("--status", dest="vcs_status", default=False,
                    help="shows a combined status command over all SCM entries",
                    action="store_true")
  parser.add_option("--status-untracked", dest="vcs_status_untracked", default=False,
                    help="shows a combined status command over all SCM entries, also showing untracked files",
                    action="store_true")
  
  parser.add_option("--generate-versioned-rosinstall", dest="generate_versioned", default=None,
                    help="generate a versioned rosinstall file", action="store")
  (options, args) = parser.parse_args(args)

  #if options.rosdep_yes:
  #  parser.error("rosinstall no longer bootstraps the build, it will not call rosmake or pass it rosdep options") 

  if options.version:
    print("rosinstall 0.5.32\n%s"%rosinstall.multiproject_cmd.cmd_version())
    sys.exit(0)
  
  if len(args) < 1:
    parser.error("rosinstall requires at least 1 argument")

  mode = 'prompt'
  if options.delete_changed:
    mode = 'delete'
  if options.abort_changed:
    if mode == 'delete':
      parser.error("delete-changed-uris is mutually exclusive with abort-changed-uris")
    mode = 'abort'
  if options.backup_changed != '':
    if mode == 'delete':
      parser.error("delete-changed-uris is mutually exclusive with backup-changed-uris")
    if mode == 'abort':
      parser.error("abort-changed-uris is mutually exclusive with backup-changed-uris")
    mode = 'backup'

  # Catkin must be enabled if catkinpp is set
  if options.catkinpp:
    options.catkin = True
  
  # Get the path to the rosinstall 
  options.path = os.path.abspath(args[0])

  config_uris = args[1:]
  
  config = rosinstall.multiproject_cmd.get_config(basepath = options.path, additional_uris = config_uris, config_filename = __ROSINSTALL_FILENAME)

  if options.generate_versioned:
    filename = os.path.abspath(options.generate_versioned)
    tree_elts = config.get_version_locked_source()
    with open(filename, 'w') as fh:
      fh.write(yaml.safe_dump(tree_elts))
    print("Saved versioned rosinstall of current directory %s to %s"%(options.path, filename))
    return 0

  if options.vcs_diff:
    alldiff = ""
    difflist = rosinstall.multiproject_cmd.cmd_diff(config, options.path)
    for entrydiff in difflist:
      if entrydiff['diff'] != None:
        alldiff += entrydiff['diff']
    print(alldiff)
    return True

  if options.vcs_status or options.vcs_status_untracked:
    statuslist = rosinstall.multiproject_cmd.cmd_status(config, options.path, untracked = options.vcs_status_untracked)
    allstatus=""
    for entrystatus in statuslist:
      if entrystatus['status'] != None:
        allstatus += entrystatus['status']
    print(allstatus)
    return True

  print("rosinstall operating on", options.path,
        "from specifications in rosinstall files ",
        ", ".join(config_uris))

  # includes ROS specific files
  rosinstall.rosinstall_cmd.cmd_persist_config_file(config)
  
  ## install or update each element
  install_success = rosinstall.multiproject_cmd.cmd_install_or_update(config, options.backup_changed, mode, options.robust)
  
  rosinstall.rosinstall_cmd.cmd_generate_ros_files(config,
                         options.path,
                         options.nobuild,
                         options.rosdep_yes,
                         catkin=True # Let it generate catkin CMakeLists.txt (this version is dated out of date), we overwrite later
                         )
  # win_ros : create setup.bat
  win_rosinstall.generate_setup(config)
  # win_ros : create toplevel.cmake->CMakeLists.txt
  shutil.copy(os.path.join(options.path,'catkin','toplevel.cmake'),
              os.path.join(options.path,'CMakeLists.txt') )

  if not install_success:
     print("Warning: installation encountered errors, but --continue-on-error was requested.  Look above for warnings.")
  return True

if __name__ == "__main__":
  try:
    sys.exit(not rosinstall_main(sys.argv))
  except ROSInstallException as e:
    sys.stderr.write("ERROR in rosinstall: %s"%str(e))
    sys.exit(1)
  except MultiProjectException as e:
    sys.stderr.write("ERROR in config: %s"%str(e))
    sys.exit(1)
