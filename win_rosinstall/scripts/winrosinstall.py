#!C:\Python27\python.exe

"""
usage: rosinstall [OPTIONS] INSTALL_PATH [ROSINSTALL FILES OR DIRECTORIES]
see: http://www.ros.org/wiki/rosinstall

Common Option:
-b or --build (perform a post install compile step)

Type 'rosinstall --help' for usage.

Common invocations:

initial checkout:   rosinstall ~/ros "http://packages.ros.org/cgi-bin/gen_rosinstall.py?rosdistro=diamondback&variant=ros-full&overlay=no"
subsequent update:  rosinstall ~/ros

"""

import os
import subprocess
import sys
from optparse import OptionParser
import yaml
import shutil
import datetime

import rosinstall.helpers

from rosinstall.vcs import VcsClient

__REPOTYPES__ = ['svn', 'bzr', 'hg', 'git']

def usage():
  print __doc__ % vars()
  exit(1)

class ROSInstallException(Exception): pass

class ConfigElement:
  """ Base class for Config provides methods with not implemented
  exceptions.  Also a few shared methods."""
  def __init__(self, path):
    self.path = path
  def get_path(self):
    return self.path
  def install(self, backup_path, mode, robust):
    raise NotImplementedError, "ConfigElement install unimplemented"
  def get_ros_path(self):
    raise NotImplementedError, "ConfigElement get_ros_path unimplemented"
  def get_yaml(self):
    """yaml with values as specified in file"""
    raise NotImplementedError, "ConfigElement get_versioned_yaml unimplemented"
  def get_versioned_yaml(self):
    raise NotImplementedError, "ConfigElement get_versioned_yaml unimplemented"
  def get_diff(self, basepath=None):
    raise NotImplementedError, "ConfigElement get_diff unimplemented"
  def get_status(self, basepath=None, untracked=False):
    raise NotImplementedError, "ConfigElement get_status unimplemented"
  def backup(self, backup_path):
    if not backup_path:
      raise ROSInstallException("Cannot install %s.  backup disabled."%self.path)
    backup_path = os.path.join(backup_path, os.path.basename(self.path)+"_%s"%datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    print "Backing up %s to %s"%(self.path, backup_path)
    shutil.move(self.path, backup_path)

def prompt_del_abort_retry(prompt, allow_skip = False):
    if allow_skip:
        valid_modes = ['(d)elete', '(a)bort', '(b)ackup', '(s)kip']
    else:
        valid_modes = ['(d)elete', '(a)bort', '(b)ackup']

    mode = ""

    full_prompt = "%s %s: "%(prompt, ", ".join(valid_modes))
  
    while mode == "":

      mode_input = raw_input(full_prompt)
      if mode_input == 'b' or mode_input == 'backup':
          mode = 'backup'
      elif mode_input == 'd' or mode_input =='delete':
          mode = 'delete'
      elif mode_input == 'a' or mode_input =='abort':
          mode = 'abort'
      elif allow_skip and mode_input == 's' or mode_input =='skip':
          mode = 'skip'
    return mode

def get_backup_path():
    backup_path = raw_input("Please enter backup pathname: ")
    print "backing up to %s"%backup_path
    return backup_path

class OtherConfigElement(ConfigElement):
  def install(self, backup_path, mode, robust=False):
    return True

  def get_ros_path(self):
    if rosinstall.helpers.is_path_ros(self.path):
      return self.path
    else:
      return None

  def get_versioned_yaml(self):
    raise ROSInstallException("Cannot generate versioned outputs with non source types")

  def get_yaml(self):
    return [{"other": {"local-name": self.path} }]
  
class VCSConfigElement(ConfigElement):
  def __init__(self, path, uri, version=''):
    self.path = path
    if uri.endswith('/'):  # strip trailing slashes to not be too strict #3061
      self.uri = uri[:-1]
    else:
      self.uri = uri
    self.version = version

  def handle_rmtree_error(self, function, path, excinfo):
    '''
      If shutil.rmtree discovers a read only file, it will spit
      the dummy on windows. So we handle it here.
    '''
    if function is os.rmdir:
      os.chmod(path, 0666)
      os.rmdir(path)
    elif function is os.remove:
      os.chmod(path,0666)
      os.remove(path)
    
  def install(self,  backup_path = None,arg_mode = 'abort', robust=False):
    mode = arg_mode
    print "Installing %s %s to %s"%(self.uri, self.version, self.path)

    # Directory exists see what we need to do
    if self.vcsc.path_exists():
      error_message = None
      if not self.vcsc.detect_presence():
        error_message = "Failed to detect %s presence at %s."%(self.vcsc.get_vcs_type_name(), self.path)
      elif not self.vcsc.get_url() or self.vcsc.get_url().rstrip('/') != self.uri.rstrip('/'):  #strip trailing slashes for #3269
        error_message = "url %s does not match %s requested."%(self.vcsc.get_url(), self.uri)
      elif (self.vcsc.get_vcs_type_name() == 'git' \
              and (self.vcsc.get_version() != self.version \
                     and self.vcsc.get_branch_parent() != self.version)):
        error_message = "The version %s of repo %s requested to be checked out into %s is not the current branch or commit and cannot be blindly updated in place."%(self.version, self.uri, self.path)
        
      # If robust ala continue-on-error, just error now and it will be continued at a higher level
      if robust and error_message:
          raise ROSInstallException(error_message)

      # prompt the user based on the error code
      if error_message:
        if arg_mode == 'prompt':
            mode = prompt_del_abort_retry(error_message, allow_skip = True)
            if mode == 'backup': # you can only backup if in prompt mode
              backup_path = get_backup_path()
        if mode == 'abort':
          raise ROSInstallException(error_message)
        elif mode == 'backup':
          self.backup(backup_path)
        elif mode == 'delete':
          shutil.rmtree(self.path, onerror=self.handle_rmtree_error)
        elif mode == 'skip':
          return
      
    # If the directory does not exist checkout
    if not self.vcsc.path_exists():
      if not self.vcsc.checkout(self.uri, self.version):
        raise ROSInstallException("Checkout of %s version %s into %s failed."%(self.uri, self.version, self.path))
      else:
        return
    else: # otherwise update
      if not self.vcsc.update(self.version):
          raise ROSInstallException("Update Failed of %s"%self.path)
      else:
          return 
    return
  
  def get_ros_path(self):
    if rosinstall.helpers.is_path_ros(self.path):
      return self.path
    else:
      return None

  def get_yaml(self):
    "yaml as from source"
    result = {self.vcsc.get_vcs_type_name(): {"local-name": self.path, "uri": self.uri} }
    if self.version != None and self.version != '':
      result[self.vcsc.get_vcs_type_name()]["version"]=self.version
    return [result]

  def get_versioned_yaml(self):
    return [{self.vcsc.get_vcs_type_name(): {"local-name": self.path, "uri": self.uri, "version":self.vcsc.get_version()} }]

  def get_diff(self, basepath=None):
    return self.vcsc.get_diff(basepath)
  
  def get_status(self, basepath=None, untracked=False):
    return self.vcsc.get_status(basepath, untracked)
  

class AVCSConfigElement(VCSConfigElement):
  def __init__(self, type, path, uri, version = ''):
    self.type = type
    self.path = path
    self.uri = uri
    self.version = version
    self.vcsc = VcsClient(self.type, self.path)


class Config:
  def __init__(self, yaml_source, install_path):
    self.source_uri = install_path #TODO Hack so I don't have to fix the usages of this remove!!!
    self.source = yaml_source
    self.trees = [ ]
    self.base_path = install_path

    if self.source:
      self.load_yaml(self.source, self.source_uri)
      self.valid = True
    else:
      self.valid = False
    
  def is_valid(self):
    return self.valid

  def load_yaml(self, y, rosinstall_source_uri):
    for t in y:
      for k, v in t.iteritems():

        # Check that local_name exists and record it
        if not 'local-name' in v:
          raise ROSInstallException("local-name is required on all rosinstall elements")
        else:
          local_name = v['local-name']

        # Get the version and source_uri elements
        source_uri = v.get('uri', None)
        version = v.get('version', '')
        
        #compute the local_path for the config element
        local_path = os.path.normpath(os.path.join(self.base_path, local_name))

        if k == 'other':
          rosinstall_uri = '' # does not exist
          if os.path.exists(local_path) and os.path.isfile(local_path):
            rosinstall_uri = local_path
          elif os.path.isdir(local_path):
            rosinstall_uri = os.path.join(local_path, ".rosinstall")
          if os.path.exists(rosinstall_uri):
            child_config = Config(rosinstall.helpers.get_yaml_from_uri(rosinstall_uri), rosinstall_uri)
            for child_t in child_config.trees:
              full_child_path = os.path.join(local_path, child_t.get_path())
              elem = OtherConfigElement(full_child_path)
              self.trees.append(elem)
          else:
            elem = OtherConfigElement(local_path)
            self.trees.append(elem)
        else:
          try:
            elem = AVCSConfigElement(k, local_path, source_uri, version)
            self.trees.append(elem)
          except LookupError as ex:
            raise ROSInstallException("Abstracted VCS Config failed. Exception: %s" % ex)

  def ros_path(self):
    rp = None
    for t in self.trees:
      ros_path = t.get_ros_path()
      if ros_path:
        rp = ros_path
    return rp
  
  def write_version_locked_source(self, filename):
    source_aggregate = []
    for t in self.trees:
      source_aggregate.extend(t.get_versioned_yaml())

    with open(filename, 'w') as fh:
      fh.write(yaml.safe_dump(source_aggregate))
      
  def write_source(self):
    """
    Write .rosinstall into the root of the checkout
    """
    if not os.path.exists(self.base_path):
      os.makedirs(self.base_path)
    f = open(os.path.join(self.base_path, ".rosinstall"), "w+b")
    f.write(
      """# THIS IS A FILE WHICH IS MODIFIED BY rosinstall
# IT IS UNLIKELY YOU WANT TO EDIT THIS FILE BY HAND
# IF YOU WANT TO CHANGE THE ROS ENVIRONMENT VARIABLES
# USE THE rosinstall TOOL INSTEAD.
# IF YOU CHANGE IT, USE rosinstall FOR THE CHANGES TO TAKE EFFECT
""")
    f.write(yaml.safe_dump(self.source))
    f.close()
    
  def execute_install(self, backup_path, mode, robust = False):
    success = True
    if not os.path.exists(self.base_path):
      os.mkdir(self.base_path)
    for t in self.trees:
      try:
        t.install(os.path.join(self.base_path, backup_path), mode)
      except ROSInstallException, ex:
        success = False
        fail_str = "Failed to install tree '%s'\n %s"%(t.get_path(), ex)
        if robust:
          print "rosinstall Continuing despite %s"%fail_str
        else:
          raise ROSInstallException(fail_str)
      else:
          pass
    return success
    # TODO go back and make sure that everything in options.path is described
    # in the yaml, and offer to delete otherwise? not sure, but it could go here

  def get_config_elements(self):
    """ Return the simplifed ROS_PACKAGE_PATH """
    code_trees = []
    for t in reversed(self.trees):
      if not rosinstall.helpers.is_path_ros(t.get_path()):
        code_trees.append(t)
    return code_trees


  def get_ros_package_path(self):
    """ Return the simplifed ROS_PACKAGE_PATH """
    code_trees = []
    for t in reversed(self.trees):
      if not rosinstall.helpers.is_path_ros(t.get_path()):
        code_trees.append(t.get_path())
    rpp = os.pathsep.join(code_trees)
    return rpp
    
  
  def generate_setup_sh_text(self, ros_root, ros_package_path):
    # overlay or standard
    text =  """#!/bin/sh
# THIS IS A FILE AUTO-GENERATED BY rosinstall
# IT IS UNLIKELY YOU WANT TO EDIT THIS FILE BY HAND
# IF YOU WANT TO CHANGE THE ROS ENVIRONMENT VARIABLES
# USE THE rosinstall TOOL INSTEAD.
# see: http://www.ros.org/wiki/rosinstall
"""
    text += "export ROS_ROOT=%s\n" % ros_root
    text += "export PATH=$ROS_ROOT/bin:$PATH\n" # might include it twice
    text += "export PYTHONPATH=$ROS_ROOT/core/roslib/src:$PYTHONPATH\n"
    text += "if [ ! \"$ROS_MASTER_URI\" ] ; then export ROS_MASTER_URI=http://localhost:11311 ; fi\n"
    text += "export ROS_PACKAGE_PATH=%s\n" % ros_package_path
    text += "export ROS_WORKSPACE=%s\n" % self.base_path
    return text

  def generate_setup_bash_text(self, shell):
    if shell == 'bash':
      script_path = """
SCRIPT_PATH="${BASH_SOURCE[0]}";
if([ -h "${SCRIPT_PATH}" ]) then
  while([ -h "${SCRIPT_PATH}" ]) do SCRIPT_PATH=`readlink "${SCRIPT_PATH}"`; done
fi
export OLDPWDBAK=$OLDPWD
pushd . > /dev/null
cd `dirname ${SCRIPT_PATH}` > /dev/null
SCRIPT_PATH=`pwd`;
popd  > /dev/null
export OLDPWD=$OLDPWDBAK
"""
    elif shell == 'zsh':
      script_path = "SCRIPT_PATH=\"$(dirname $0)\";"
    else:
      raise ROSInstallException("%s shell unsupported."%shell);

    text =  """#!/bin/%(shell)s
# THIS IS A FILE AUTO-GENERATED BY rosinstall
# IT IS UNLIKELY YOU WANT TO EDIT THIS FILE BY HAND
# IF YOU WANT TO CHANGE THE ROS ENVIRONMENT VARIABLES
# USE THE rosinstall TOOL INSTEAD.
# see: http://www.ros.org/wiki/rosinstall


# Load the path of this particular setup.%(shell)s                                                                                                                  
%(script_path)s

. $SCRIPT_PATH/setup.sh

if [ -e ${ROS_ROOT}/tools/rosbash/ros%(shell)s ]; then
  . ${ROS_ROOT}/tools/rosbash/ros%(shell)s
fi
"""%locals()
    return text
    
  def generate_setup_bat_text(self, ros_root, ros_package_path):
    # overlay or standard
    text =  """
REM This is a file auto-generated by rosinstall for windows
REM refer to http://code.google.com/p/win-ros-pkg/wiki/WinRosinstall
REM for more information.
"""
    pythonhome = sys.exec_prefix
    pythonscripts = os.path.join(pythonhome,'Scripts')
    pythonpath = os.path.join(ros_root,'core','roslib','src')
    ros_root_bin = os.path.join(ros_root,'bin')
    text += "\n"
    text += "ECHO OFF\n"
    text += "\n"
    text += "set PYTHONHOME=%s\n"%pythonhome
    text += "set PYTHONPATH=%s\n"%pythonpath
    text += "set PATH=%s"%pythonscripts+os.pathsep+"%PATH%\n" 
    text += "\n"
    text += "set ROS_ROOT=%s\n" % ros_root
    text += "set ROS_PACKAGE_PATH=%s\n" % ros_package_path
    text += "set ROS_WORKSPACE=%s\n" % self.base_path
    text += "set PATH=%s"%ros_root_bin+os.pathsep+"%PATH%\n" 
    text += "\n"
    text += "set ROS_MASTER_URI=http://localhost:11311\n"
    text += "REM set ROS_IP=192.168.10.231\n"
    text += "REM set ROS_HOSTNAME=concert_master\n"
    text += "\n"
    text += "REM Utilitiy variables\n"
    text += 'doskey wordpad="'+os.environ['PROGRAMFILES']+'\\Windows NT\\Accessories\\wordpad.exe" $1\n'
    text += "REM This isn't fully supported yet\n"
    text += 'REM doskey roscd=%s\\win_ros\\win_roscd\\roscd.bat $1\n'%self.base_path
    text += "\n"
    text += "REM Rosbuild2 variables\n"
    text += "set PATH="+os.environ['PROGRAMFILES']+"\\boost\\boost_1_44\\lib"+os.pathsep+"%PATH%\n"
    text += "\n"
    text += "REM Environment settings for your compiler [MS Express]\n"
    text += '"'+os.environ['PROGRAMFILES']+'\\Microsoft Visual Studio 10.0\\VC\\vcvarsall.bat"\n'
    text += "REM Environment settings for your compiler [Windows SDK][Experimental]\n"
    text += 'REM "C:\Program Files\Microsoft SDKs\Windows\v7.1\Bin\SetEnv.cmd"'
    text += "\n"
    return text

  def generate_setup(self):
    # simplest case first
    ros_root = self.ros_path()
    if not ros_root:
      raise ROSInstallException("No 'ros' stack detected.  The 'ros' stack is required in all rosinstall directories. Please add a definition of the 'ros' stack either manually in .rosinstall and then call 'rosinstall .' in the directory. Or add one on the command line 'rosinstall . http://www.ros.org/rosinstalls/boxturtle_ros.rosinstall'. Or reference an existing install like in /opt/ros/boxturtle with 'rosinstall . /opt/ros/boxturtle'.  Note: the above suggestions assume you are using boxturtle, if you are using latest or another distro please change the urls." )
    rpp = self.get_ros_package_path()
    
    text = self.generate_setup_bat_text(ros_root, rpp)
    setup_path = os.path.join(self.base_path, 'setup.bat')
    with open(setup_path, 'w') as f:
      f.write(text)

    text = self.generate_setup_sh_text(ros_root, rpp)
    setup_path = os.path.join(self.base_path, 'setup.sh')
    with open(setup_path, 'w') as f:
      f.write(text)

    for shell in ['bash', 'zsh']:
      text = self.generate_setup_bash_text(shell)
      setup_path = os.path.join(self.base_path, 'setup.%s'%shell)
      with open(setup_path, 'w') as f:
        f.write(text)

## legacy for breadcrumb which will be removed shortly.
def installed_uri(path):
  try:
    f = open(os.path.join(path, '.rosinstall_source_uri'),'r')
    print "Falling back onto deprecated .rosinstall_source_uri"
  except IOError as e:
    return None
  return rosinstall.helpers.conditional_abspath(f.readline())  # abspath here for backwards compatibility with change to abspath in breadcrumb


def insert_source_yaml(source_yaml, source, observed_paths, aggregate_source_yaml):
    if source_yaml:
      for element in source_yaml:
        #print "element", element
        for k in element:
          #print "element[k]", element[k]
          if not element[k]:
              raise ROSInstallException("Malformed rosinstall source: %s  An \"%s\" entry is present without any information.  This can be caused by improper indentation of fields like 'local-name'. "%(source, k))
          if 'local-name' in element[k]:
            path = element[k]['local-name']
            if path in observed_paths:
              #print "local-name '%s' redefined, first definition in %s, second definition in %s"%(path, observed_paths[path], source)
              overlapping = []
              for agel in aggregate_source_yaml:
                for vcs_type in agel:
                  for param in agel[vcs_type]:
                    #print "param", param
                    if param == "local-name" and agel[vcs_type]['local-name'] == path:
                      overlapping.append(agel)
              #print "OVERLAPPING", overlapping
              for ol in overlapping:
                #print "removing: ", ol
                aggregate_source_yaml.remove(ol)

            observed_paths[path] = source
          else:  
            return "local-name must be defined for all targets, failed in %s"%source
      aggregate_source_yaml.extend(source_yaml)
      
      return ''

def rewrite_included_source(source_yaml, source_path):
  #print "before", source_yaml
  for entry in source_yaml:
    types = ['svn', 'bzr', 'hg', 'git', 'other']
    for t in types:
      if t in entry.keys():
        local_path = os.path.join(source_path, entry[t]['local-name'])
        del entry[t]
        entry['other'] = {}
        entry['other']['local-name'] = local_path
  #print "after", source_yaml
  return source_yaml


def get_diffs(config, path):
  """calls SCM diff for all SCM entries in config, relative to path"""
  result=[]

  for element in config.get_config_elements():
    entry = element.get_yaml()[0]
    for scmtype in __REPOTYPES__:
      if scmtype in entry.keys():
        result.append({'entry':entry, 'diff':element.get_diff(path)})
  return result


def get_statuses(config, path, untracked = False):
  """calls SCM status for all SCM entries in config, relative to path"""
  result=[]
  for element in config.get_config_elements():
    entry = element.get_yaml()[0]
    for scmtype in __REPOTYPES__:
      if scmtype in entry.keys():
        status = element.get_status(path, untracked)
        # align other scm output to svn
        columns = -1
        if scmtype == "git":
          columns = 3
        elif scmtype == "hg":
          columns = 2
        elif scmtype == "bzr":
          columns = 4
        if columns > -1 and status != None:
          status_aligned = ''
          for line in status.splitlines():
            status_aligned = status_aligned + line[:columns].ljust(8) + line[columns:] + '\n'
          status = status_aligned
        result.append({'entry':entry, 'status':status})
  return result


def rosinstall_main(argv):
  if len(argv) < 2:
    usage()
  args = argv[1:]
  parser = OptionParser(usage="usage: rosinstall [OPTIONS] INSTALL_PATH [ROSINSTALL FILES OR DIRECTORIES]\n\n\
rosinstall does the following:\n\
  1. Merges all URIs into new or existing .rosinstall file at PATH\n\
  2. Checks out or updates all version controlled URIs\n\
  3. Calls rosmake after checkout or updates\n\
  4. Generates/overwrites updated setup files\n\n\
URIs can be web urls to remote .rosinstall files, local .rosinstall files,\n\
git, svn, bzr, hg URIs, or local directories.\n\
Later URIs will shadow packages of earlier URIs.\n",
                        epilog="See: http://www.ros.org/wiki/rosinstall for details\n",
                        version="%prog 0.5.24")
  parser.add_option("-b", "--build", dest="build", default=False,
                    help="perform a post install build step for the ROS stack",
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
    

  # Get the path to the rosinstall 
  options.path = os.path.abspath(args[0])

  # Find out what the URI is (args, .rosinstall, or breadcrumb(for backwards compatability)
  config_uris = []

  if os.path.exists(os.path.join(options.path, ".rosinstall")):
    config_uris.append(os.path.join(options.path, ".rosinstall"))
  else: ## backwards compatability to be removed in the future
    # try to read the source uri from the breadcrumb mmmm delicious
    config_uri = installed_uri(options.path)
    if config_uri:
      config_uris.append(config_uri)

  config_uris.extend(args[1:])

  other_source = """- other: 
    local-name: %s
"""

  observed_paths = {}
  aggregate_source_yaml = []

  for a in config_uris:
    #print "argument", a
    config_uri = rosinstall.helpers.conditional_abspath(a)
    if os.path.isdir(config_uri):
      rosinstall_uri = os.path.join(config_uri, ".rosinstall")
      #print "processing config_uri %s"%config_uri
      if os.path.exists(rosinstall_uri):
        source_yaml = rosinstall.helpers.get_yaml_from_uri(rosinstall_uri)
        if not source_yaml:
          raise ROSInstallException("Bad remote rosinstall source: %s  This can be caused by empty or malformed remote rosinstall file. "%(a))
        source_yaml = rewrite_included_source(source_yaml, config_uri)
      else:
        # fall back to just a directory
        source_yaml = [ {'other': {'local-name': '%s'%config_uri} } ]
    else:
      source_yaml = rosinstall.helpers.get_yaml_from_uri(config_uri)
      if not source_yaml:
          raise ROSInstallException("Bad remote rosinstall source: %s  This can be caused by empty or malformed remote rosinstall file. "%(a))
    #print "source yaml", source_yaml
    result = insert_source_yaml(source_yaml, a, observed_paths, aggregate_source_yaml)
    if result != '':
      parser.error(result)

  ## Could not get uri therefore error out
  if len(config_uris) == 0:
    parser.error( "no source rosinstall file found! looked at arguments, %s , and %s(deprecated)"%(
        os.path.join(options.path, ".rosinstall"), os.path.join(options.path, ".rosinstall_source_uri")))

  #print "source...........................", aggregate_source_yaml

  ## Generate the config class with the uri and path
  config = Config(aggregate_source_yaml, options.path)
  if not config.is_valid():
    return -1

  if options.generate_versioned:
    filename = os.path.abspath(options.generate_versioned)
    config.write_version_locked_source(filename)
    print "Saved versioned rosinstall of current directory %s to %s"%(options.path, filename)
    return 0

  if options.vcs_diff:
    alldiff = ""
    difflist = get_diffs(config, options.path)
    for entrydiff in difflist:
      if entrydiff['diff'] != None:
        alldiff += entrydiff['diff']
    print alldiff
    return True

  if options.vcs_status:
    statuslist = get_statuses(config, options.path, False)

    allstatus=""
    for entrystatus in statuslist:
      if entrystatus['status'] != None:
        allstatus += entrystatus['status']
    print allstatus
    return True

  if options.vcs_status_untracked:
    statuslist = get_statuses(config, options.path, True)

    allstatus=""
    for entrystatus in statuslist:
      if entrystatus['status'] != None:
        allstatus += entrystatus['status']
    print allstatus
    return True

  print "rosinstall operating on", options.path, "from specifications in rosinstall files ", ", ".join(config_uris)

  ## Save .rosinstall 
  config.write_source()
  ## install or update each element
  install_success = config.execute_install(options.backup_changed, mode, options.robust)
  ## Generate setup.sh and save
  config.generate_setup()
  ## Prep for rosbuild2 if found
  rpp = config.get_ros_package_path().split(os.pathsep)
  bootstrap_rosbuild2 = False
  for path in rpp:
    if os.path.basename(path) == 'cmake':
      print "Prepping for rosbuild2"
      shutil.copy(os.path.join(path,'CMakeLists.txt'),
                os.path.join(config.base_path,'CMakeLists.txt') )
      bootstrap_rosbuild2 = True
      break
  ## bootstrap the build if installing ros
  if config.ros_path() and options.build:
    print "Bootstrapping ROS build"
    rosdep_yes_insert = ""
    if options.rosdep_yes:
      rosdep_yes_insert = " --rosdep-yes"
    ros_comm_insert = ""
    if 'ros_comm' in [os.path.basename(tree.path) for tree in config.trees]:
      print "Detected ros_comm bootstrapping it too."
      ros_comm_insert = " ros_comm"
    subprocess.check_call("source %s && rosmake ros%s --rosdep-install%s" % (os.path.join(options.path, 'setup.sh'), ros_comm_insert, rosdep_yes_insert), shell=True, executable='/bin/bash')
    print "\nrosinstall update complete.\n\nNow, type 'source %s/setup.bash' to set up your environment.\nAdd that to the bottom of your ~/.bashrc to set it up every time.\n\nIf you are not using bash please see http://www.ros.org/wiki/rosinstall/NonBashShells " % options.path

  if not install_success:
     print "Warning: installation encountered errors, but --continue-on-error was requested.  Look above for warnings."
  return True

if __name__ == "__main__":
  try:
    sys.exit(not rosinstall_main(sys.argv))
  except ROSInstallException as e:
    print >> sys.stderr, "ERROR: %s"%str(e)
    sys.exit(1)

