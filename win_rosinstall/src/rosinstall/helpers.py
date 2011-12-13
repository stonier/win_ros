# Software License Agreement (BSD License)
#
# Copyright (c) 2010, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import urlparse
import urllib2
import yaml
import subprocess
import sys

def conditional_abspath(uri):
  """
  @param uri: The uri to check
  @return: abspath(uri) if local path otherwise pass through uri
  """
  u = urlparse.urlparse(uri)
  if u.scheme == '': # maybe it's a local file?
    return os.path.abspath(uri)
  else:
    return uri

def is_path_stack(path):
  """
  
  @return: True if the path provided is the root of a stack.
  """
  stack_path = os.path.join(path,'stack.xml')
  if os.path.isfile(stack_path):
    return True
  return False

def is_path_ros(path):
  """
  warning: exits with code 1 if stack document is invalid
  @param path: path of directory to check
  @type  path: str
  @return: True if path points to the ROS stack
  @rtype: bool
  """
  stack_path = os.path.join(path,'stack.xml')
  if os.path.isfile(stack_path):
    return 'ros' == os.path.basename(path)
  return False


def get_yaml_from_uri(uri):

  # now that we've got a config uri and a path, let's move out.
  f = 0
  if os.path.isfile(uri):
    try:
      f = open(uri, 'r')
    except IOError as e:
      sys.stderr.write("error opening file [%s]: %s\n" % (uri, e))
      return None
  else:
    try:
      f = urllib2.urlopen(uri)
    except IOError as e:
      sys.stderr.write("Is not a local file, nor able to download as a URL [%s]: %s\n" % (uri, e))
    except ValueError as e:
      sys.stderr.write("Is not a local file, nor a valid URL [%s] : %s\n" % (uri,e))
  if not f:
    sys.stderr.write("couldn't load config uri %s\n" % uri)
    return None
  try:
    y = yaml.load(f);
  except yaml.YAMLError as e:
    sys.stderr.write("Invalid rosinstall yaml format in [%s]: %s\n" % (uri, e ))
    return None
  return y
  
