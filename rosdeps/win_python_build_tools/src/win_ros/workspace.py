# Software License Agreement (BSD License)
#
# Copyright (c) 2013, Yujin Robot, Inc.
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
#  * Neither the name of Yujin Robot nor the names of its
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

##############################################################################
# Imports
##############################################################################

import sys
import os
import urllib2

##############################################################################
# Constants
##############################################################################

# These are used to flip between stable/unstable downloads
STABLE =  0
UNSTABLE = 1

toplevel_cmake_url = { 
    UNSTABLE : 'https://raw.github.com/ros/catkin/groovy-devel/cmake/toplevel.cmake', 
    STABLE : 'https://raw.github.com/ros/catkin/3deda412ff09f94a5658a582062b22a8926c0b75/cmake/toplevel.cmake'
    }

##############################################################################
# Private Functions
##############################################################################

def generate_setup_bat_text():
    # overlay or standard
    text =  """
REM This is a file auto-generated to assist in a usable win-ros
REM command line environment.
"""
    home_drive = os.environ['HOMEDRIVE']
    program_files = home_drive + r'\Program Files'
    program_files_x86 = home_drive + r'\Program Files (x86)'
    windows_sdk_env = program_files + r'\Microsoft SDKs\Windows\v7.1\Bin\SetEnv.cmd';
    visual_studio_ten_env = program_files + r'\Microsoft Visual Studio 10.0\VC\vcvarsall.bat';
    visual_studio_ten_env_x86 = program_files_x86 + r'\Microsoft Visual Studio 10.0\VC\vcvarsall.bat';
    wordpad_path = program_files + r'\Windows NT\Accessories\wordpad.exe';
    wordpad_path_x86 = program_files_x86 + r'\Windows NT\Accessories\wordpad.exe';
    notepp_path = program_files + r'\Notepad++\notepad++.exe';
    notepp_path_x86 = program_files_x86 + r'\Notepad++\notepad++.exe';
    
    text += "\n"
    text += "@REM Utility variables\n"
    if os.path.isfile(wordpad_path):
        text += '@doskey wordpad="'+wordpad_path+'" $1\n'
    else:
        text += '@doskey wordpad="'+wordpad_path_x86+'" $1\n'
    if os.path.isfile(notepp_path):
        text += '@doskey notepp="'+notepp_path+'" $1\n'
    elif os.path.isfile(notepp_path_x86):
        text += '@doskey notepp="'+notepp_path_x86+'" $1\n'
    else:
        text += '@REM doskey notepp="'+notepp_path+'" $1\n'
    text += "\n"
    if os.path.isfile(windows_sdk_env):
        text += "@REM Environment settings for Windows SDK\n"
        text += '@call "' + windows_sdk_env + '" /x86 /Release\n'
        text += "@REM The sdk is the default generator for winros,\n"
        text += "@REM To use visual studio, uncomment one of the following.\n"
        text += '@REM "' + visual_studio_ten_env + '" x86\n'
        text += '@REM "' + visual_studio_ten_env_x86 + '" x86\n'
    elif os.path.isfile(visual_studio_ten_env):
        text += "@REM Environment settings for Visual Studio\n"
        text += '@call "' + visual_studio_ten_env + '" x86\n'
        text += '@REM call "' + windows_sdk_env + '" /x86 /Release\n'
    elif os.path.isfile(visual_studio_ten_env_x86):
        text += "@REM Environment settings for Visual Studio\n"
        text += '@call "' + visual_studio_ten_env_x86 + '" x86\n'
        text += '@REM call "' + windows_sdk_env + '" /x86 /Release\n'
    else:
        text += "@REM Could not find windows sdk or visual studio, please\n"
        text += "@REM install and configure by hand [Windows SDK/Visual Studio]\n"
        text += '@REM call "' + windows_sdk_env + '" /x86 /Release\n'
        text += '@REM "' + visual_studio_ten_env + '" x86\n'
        text += '@REM "' + visual_studio_ten_env_x86 + '" x86\n'
    text += '@REM Colours are a god awful ugly canary yellow or vomit green\n'
    text += '@color 7\n'
    text += "\n"
    return text

##############################################################################
# Public Functions
##############################################################################


def write_setup_bat(base_path):
    text = generate_setup_bat_text()
    setup_path = os.path.join(base_path, 'setup.bat')
    with open(setup_path, 'w') as f:
        f.write(text)


def write_toplevel_cmake(base_path, distro = STABLE):

    u = urllib2.urlopen( toplevel_cmake_url[distro] )
    local_file = open(os.path.join(base_path, 'CMakeLists.txt'), 'w')
    local_file.write(u.read())
    local_file.close()