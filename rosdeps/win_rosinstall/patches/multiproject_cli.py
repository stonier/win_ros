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

from __future__ import print_function
import sys
import os
import textwrap
import shutil
from optparse import OptionParser, IndentedHelpFormatter
from common import samefile, select_element, select_elements, MultiProjectException
from config_yaml import PathSpec

import multiproject_cmd

# implementation of single CLI commands (extracted for use in several overlapping scripts)

__MULTIPRO_CMD_DICT__={
  "help"     : "provide help for commands",
  "init"     : "set up a directory as workspace",
  "info"     : "Overview of some entries",
  "merge"    : "merges your workspace with another config set",
  "set"      : "add or changes one entry from your workspace config",
  "update"   : "update or check out some of your config elements",
  "remove"   : "remove an entry from your workspace config, without deleting files",
  "snapshot" : "write a file specifying repositories to have the version they currently have",
  "diff"     : "print a diff over some SCM controlled entries",
  "status"   : "print the change status of files in some SCM controlled entries",
}

class IndentedHelpFormatterWithNL(IndentedHelpFormatter):
    def format_description(self, description):
        if not description: return ""
        desc_width = self.width - self.current_indent
        indent = " "*self.current_indent
        # the above is still the same
        bits = description.split('\n')
        formatted_bits = [
            textwrap.fill(bit,
                          desc_width,
                          initial_indent=indent,
                          subsequent_indent=indent)
            for bit in bits]
        result = "\n".join(formatted_bits) + "\n"
        return result 


def _get_mode_from_options(parser, options):
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
    return mode

  

class MultiprojectCLI:

    def __init__(self, config_filename = None):
        self.config_filename = config_filename

    # def cmd_init(self, argv):
    #     raise Exception("Not implemented yet")
    # TODO enable when making multiproject an independent CLI

    
    # def cmd_merge(self, target_path, argv, config = None):
    #     raise Exception("Not implemented yet")
    # TODO enable when making multiproject an independent CLI


    def cmd_diff(self, target_path, argv, config = None):
        parser = OptionParser(usage="usage: rosws diff [localname]* ",
                              description=__MULTIPRO_CMD_DICT__["diff"],
                              epilog="See: http://www.ros.org/wiki/rosinstall for details\n")
        # required here but used one layer above
        parser.add_option("-t", "--target-workspace", dest="workspace", default=None,
                          help="which workspace to use",
                          action="store")
        (options, args) = parser.parse_args(argv)
        
        if config == None:
            config = multiproject_cmd.get_config(target_path, [], config_filename = self.config_filename)
        elif config.get_base_path() != target_path:
            raise MultiProjectException("Config path does not match %s %s "%(config.get_base_path(), target_path))

        
        if len(args) > 0:
            difflist = multiproject_cmd.cmd_diff(config, localnames = args)
        else:
            difflist = multiproject_cmd.cmd_diff(config)
        alldiff = ""
        for entrydiff in difflist:
            if entrydiff['diff'] != None:
                alldiff += entrydiff['diff']
        print(alldiff)
            
        return False
    
    
    def cmd_status(self, target_path, argv, config = None):
        parser = OptionParser(usage="usage: rosws status [localname]* ",
                              description=__MULTIPRO_CMD_DICT__["status"] + ". The status columns meanings are as the respective SCM defines them.",
                              epilog="""See: http://www.ros.org/wiki/rosinstall for details""")
        parser.add_option("--untracked", dest="untracked", default=False,
                          help="Also shows untracked files",
                          action="store_true")
        # -t option required here for help but used one layer above, see cli_common
        parser.add_option("-t", "--target-workspace", dest="workspace", default=None,
                          help="which workspace to use",
                          action="store")
        (options, args) = parser.parse_args(argv)
    
        if config == None:
            config = multiproject_cmd.get_config(target_path, [], config_filename = self.config_filename)
        elif config.get_base_path() != target_path:
            raise MultiProjectException("Config path does not match %s %s "%(config.get_base_path(), target_path))

        if len(args) > 0:
            statuslist = multiproject_cmd.cmd_status(config,
                                                     localnames = args,
                                                     untracked = options.untracked)
        else:
            statuslist = multiproject_cmd.cmd_status(config, untracked = options.untracked)
        allstatus=""
        for entrystatus in statuslist:
            if entrystatus['status'] != None:
                allstatus += entrystatus['status']
        print(allstatus)
        return 0

    
    def cmd_set(self, target_path, argv, config = None):
        """
        command for modifying/adding a single entry
        :param target_path: where to look for config
        :param config: config to use instead of parsing file anew
        """
        parser = OptionParser(usage="usage: rosws set [localname] [SCM-URI]?  [--(detached|svn|hg|git|bzr)] [--version=VERSION]]",
                              formatter = IndentedHelpFormatterWithNL(),
                              description=__MULTIPRO_CMD_DICT__["set"] + """
The command will infer whether you want to add or modify an entry. If
you modify, it will only change the details you provide, keeping
those you did not provide. if you only provide a uri, will use the
basename of it as localname unless such an element already exists.

The command only changes the configuration, to checkout or update
the element, run rosws update afterwards.

Examples:
$ rosws set robot_model --hg https://kforge.ros.org/robotmodel/robot_model
$ rosws set robot_model --version robot_model-1.7.1
$ rosws set robot_model --detached
""",
                              epilog="See: http://www.ros.org/wiki/rosinstall for details\n")
        parser.add_option("--detached", dest="detach", default=False,
                          help="make an entry unmanaged (default for new element)",
                          action="store_true")
        parser.add_option("-v","--version-new", dest="version", default=None,
                          help="point SCM to this version",
                          action="store")
        parser.add_option("--git", dest="git", default=False,
                          help="make an entry a git entry",
                          action="store_true")
        parser.add_option("--svn", dest="svn", default=False,
                          help="make an entry a subversion entry",
                          action="store_true")
        parser.add_option("--hg", dest="hg", default=False,
                          help="make an entry a mercurial entry",
                          action="store_true")
        parser.add_option("--bzr", dest="bzr", default=False,
                          help="make an entry a bazaar entry",
                          action="store_true")
        parser.add_option("-y", "--confirm", dest="confirm", default='',
                          help="Do not ask for confirmation",
                          action="store_true")
        # -t option required here for help but used one layer above, see cli_common
        parser.add_option("-t", "--target-workspace", dest="workspace", default=None,
                          help="which workspace to use",
                          action="store")
        (options, args) = parser.parse_args(argv)

        if len(args) > 2:
            print("Error: Too many arguments.")
            print(parser.usage)
            return -1
        
        if config == None:
            config = multiproject_cmd.get_config(target_path, [], config_filename = self.config_filename)
        elif config.get_base_path() != target_path:
            raise MultiProjectException("Config path does not match %s %s "%(config.get_base_path(), target_path))

        scmtype = None
        count_scms = 0
        if options.git:
            scmtype = 'git'
            count_scms +=1
        if options.svn:
            scmtype = 'svn'
            count_scms +=1
        if options.hg:
            scmtype = 'hg'
            count_scms +=1
        if options.bzr:
            scmtype = 'bzr'
            count_scms +=1
        if options.detach:
            count_scms +=1
        if count_scms > 1:
            parser.error("You cannot provide more than one scm provider option")
          
        if len(args) == 0:
            parser.error("Must provide a localname")
        
        element = select_element(config.get_config_elements(), args[0])

        uri = None
        if len(args) == 2:
            uri = args[1]
        version = None
        if options.version is not None:
            version = options.version.strip("'\"")
        
        if element is None:
            # asssume is insert, choose localname
            localname = os.path.normpath(args[0])
            rel_path = os.path.relpath(os.path.realpath(localname),
                                       os.path.realpath(config.get_base_path()))
            if os.path.isabs(localname):
                # use shorter localname for folders inside workspace
                if not rel_path.startswith('..'):
                    localname = rel_path
            else:
                # got a relative path as localname, could point to a dir or be meant relative to workspace
                if not samefile(os.getcwd(), config.get_base_path()):
                    if os.path.isdir(localname):
                        parser.error("Cannot decide which one you want to add:\n%s\n%s"%(os.path.abspath(localname),
                                                                                         os.path.join(config.get_base_path(), localname)))
                    if not rel_path.startswith('..'):
                        localname = rel_path

            spec = PathSpec(local_name = localname,
                            uri = uri,
                            version = version,
                            scmtype = scmtype)
            print("     Add element: \n %s"%spec)
        else:
            # modify
            old_spec = element.get_path_spec()
            if options.detach:
                spec = PathSpec(local_name = element.get_local_name())
            else:
                # '' evals to False, we do not want that
                if version is None:
                    version = old_spec.get_version()
                spec = PathSpec(local_name = element.get_local_name(),
                                uri = uri or old_spec.get_uri(),
                                version = version,
                                scmtype = scmtype or old_spec.get_scmtype(),
                                path = old_spec.get_path())
            if spec.get_legacy_yaml() == old_spec.get_legacy_yaml():
                if not options.detach:
                    parser.error("No change provided, did you mean --detach ?")
                parser.error("No change provided.")
            print("     Change element from: \n %s\n     to\n %s"%(old_spec, spec))

        config.add_path_spec(spec, merge_strategy = 'MergeReplace')
        if not options.confirm:
            abort = None
            prompt = "Continue(y/n): "
            while abort == None:
                mode_input = raw_input(prompt)
                if mode_input == 'y':
                    abort = False
                elif mode_input == 'n':
                    abort = True
            if abort:
                print("No changes made.")
                return 0
        print("Overwriting %s"%os.path.join(config.get_base_path(), self.config_filename))
        shutil.move(os.path.join(config.get_base_path(), self.config_filename), "%s.bak"%os.path.join(config.get_base_path(), self.config_filename))
        multiproject_cmd.cmd_persist_config(config, self.config_filename)

        if (spec.get_scmtype() is not None):
          print("Config changed, remember to run 'rosws update %s' to update the folder from %s"%(spec.get_local_name(), spec.get_scmtype()))
        # for element in config.get_config_elements():
        #   if element.get_local_name() == spec.get_local_name():
        #     if element.is_vcs_element():
        #       element.install(checkout = not os.path.exists(os.path.join(config.get_base_path(), spec.get_local_name())))
        #       break
        return 0


    def cmd_update(self, target_path, argv, config = None):
        parser = OptionParser(usage="usage: rosws update [localname]*",
                              formatter = IndentedHelpFormatterWithNL(),
                              description=__MULTIPRO_CMD_DICT__["update"] + """

This command calls the SCM provider to pull changes from remote to
your local filesystem. In case the url has changed, the command will
ask whether to delete or backup the folder.

Examples:
$ rosws update -t ~/fuerte
$ rosws update robot_model geometry
""",
                              epilog="See: http://www.ros.org/wiki/rosinstall for details\n")
        parser.add_option("--delete-changed-uris", dest="delete_changed", default=False,
                          help="Delete the local copy of a directory before changing uri.",
                          action="store_true")
        parser.add_option("--abort-changed-uris", dest="abort_changed", default=False,
                          help="Abort if changed uri detected",
                          action="store_true")
        parser.add_option("--continue-on-error", dest="robust", default=False,
                          help="Continue despite checkout errors",
                          action="store_true")
        parser.add_option("--backup-changed-uris", dest="backup_changed", default='',
                          help="backup the local copy of a directory before changing uri to this directory.",
                          action="store")
        parser.add_option("-j", "--parallel", dest="jobs", default=1,
                          help="How many parallel threads to use for installing",
                          action="store")
        parser.add_option("-v", "--verbose", dest="verbose", default=False,
                          help="Whether to print out more information",
                          action="store_true")
        # -t option required here for help but used one layer above, see cli_common
        parser.add_option("-t", "--target-workspace", dest="workspace", default=None,
                          help="which workspace to use",
                          action="store")
        (options, args) = parser.parse_args(argv)

        if config == None:
            config = multiproject_cmd.get_config(target_path, [], config_filename = self.config_filename)
        elif config.get_base_path() != target_path:
            raise MultiProjectException("Config path does not match %s %s "%(config.get_base_path(), target_path))
        success = True
        mode = _get_mode_from_options(parser, options)
        if args == []:
            # None means no filter, [] means filter all
            args = None
        if success:
            install_success = multiproject_cmd.cmd_install_or_update(
              config,
              localnames = args,
              backup_path = options.backup_changed,
              mode = mode,
              robust = options.robust,
              num_threads = int(options.jobs),
              verbose = options.verbose)
            if install_success or options.robust:
                return 0
        return 1


    def cmd_remove(self, target_path, argv, config = None):
        parser = OptionParser(usage="usage: rosws remove [localname]*",
                              formatter = IndentedHelpFormatterWithNL(),
                              description=__MULTIPRO_CMD_DICT__["remove"] + """
The command removes entries from your configuration file, it does not affect your filesystem.
""",
                              epilog="See: http://www.ros.org/wiki/rosinstall for details\n")
        (options, args) = parser.parse_args(argv)
        if len(args) < 1:
            print("Error: Too few arguments.")
            print(parser.usage)
            return -1

        if config == None:
            config = multiproject_cmd.get_config(target_path, [], config_filename = self.config_filename)
        elif config.get_base_path() != target_path:
            raise MultiProjectException("Config path does not match %s %s "%(config.get_base_path(), target_path))
        success = True
        elements = select_elements(config, args)
        for element in elements:
            if not config.remove_element(element.get_local_name()):
                success = False
                print("Bug: No such element %s in config, aborting without changes"%(element.get_local_name()))
                break
        if success:
            print("Overwriting %s"%os.path.join(config.get_base_path(), self.config_filename))
            shutil.move(os.path.join(config.get_base_path(), self.config_filename), "%s.bak"%os.path.join(config.get_base_path(), self.config_filename))
            multiproject_cmd.cmd_persist_config(config, self.config_filename)
            print("Removed entries %s"%args)
            
        return 0

    # def cmd_info(self, target_path, argv, reverse = False, config = None):
    #     """
    #     :param target_path: where to look for config
    #     :param config: config to use instead of parsing file anew
    #     """
    #     __pychecker__ = 'unusednames=reverse'
    #     raise Exception("Not implemented yet")
    # TODO enable when making multiproject an independent CLI


    def _get_element_diff(self, new_path_spec, config_old, extra_verbose = False):
        """
        :returns: a string telling what changed for element compared to old config
        """
        if new_path_spec is None or config_old is None:
            return ''
        output = ' %s'%new_path_spec.get_local_name()
        if extra_verbose:
            old_element = None
            if config_old is not None:
                old_element = select_element(config_old.get_config_elements(), new_path_spec.get_local_name())

            if old_element is None:
                if new_path_spec.get_scmtype() is not None:
                  output += "   \t%s  %s   %s"%(new_path_spec.get_scmtype(), new_path_spec.get_uri(), new_path_spec.get_version() or '')
            else:
                old_path_spec = old_element.get_path_spec()
                for attr in new_path_spec.__dict__:
                    if (attr in old_path_spec.__dict__
                        and old_path_spec.__dict__[attr] != new_path_spec.__dict__[attr]
                        and attr[1:] not in ['local_name', 'path']):
                      old_val = old_path_spec.__dict__[attr]
                      new_val = new_path_spec.__dict__[attr]
                      
                      commonprefix = new_val[:[x[0]==x[1] for x in zip(str(new_val), str(old_val))].index(0)]
                      if len(commonprefix) > 11:
                          new_val = "...%s"%new_val[len(commonprefix)-7:]
                      output += "  \t%s: %s -> %s;"%(attr[1:], old_val, new_val)
                    else:
                      if (attr not in old_path_spec.__dict__
                          and new_path_spec.__dict__[attr] is not None
                          and new_path_spec.__dict__[attr] != ""
                          and new_path_spec.__dict__[attr] != []
                          and attr[1:] not in ['local_name', 'path']):
                        output += "  %s = %s"%(attr[1:], new_path_spec.__dict__[attr])
        return output
          

    def prompt_merge(self,
                     target_path,
                     additional_uris,
                     additional_specs,
                     path_change_message = None,
                     merge_strategy = 'KillAppend',
                     confirmed = False,
                     config = None):
        """
        Prompts the user for the resolution of a merge
        
        :param target_path: Location of the config workspace
        :param additional_uris: what needs merging in
        :returns: tupel (Config or None if no change, bool path_changed)
        """
        if config == None:
            config = multiproject_cmd.get_config(target_path, additional_uris = [], config_filename = self.config_filename)
        elif config.get_base_path() != target_path:
            raise MultiProjectException("Config path does not match %s %s "%(config.get_base_path(), target_path))
        local_names_old = [x.get_local_name() for x in config.get_config_elements()]

        extra_verbose = confirmed
        abort = None
        last_merge_strategy = None
        while abort == None:

            if (last_merge_strategy is None
                or last_merge_strategy != merge_strategy):
              newconfig = multiproject_cmd.get_config(target_path, additional_uris = [], config_filename = self.config_filename)
              config_actions = multiproject_cmd.add_uris(newconfig,
                                                         additional_uris = additional_uris,
                                                         merge_strategy = merge_strategy)
              for path_spec in additional_specs:
                  action = newconfig.add_path_spec(path_spec, merge_strategy)
                  config_actions[path_spec.get_local_name()] = (action, path_spec)
              last_merge_strategy = merge_strategy
            
            local_names_new = [x.get_local_name() for x in newconfig.get_config_elements()]
            
            path_changed = False
            ask_user = False
            output = ""
            new_elements = []
            changed_elements = []
            discard_elements = []
            for localname, (action, new_path_spec) in config_actions.items():
                index = -1
                if localname in local_names_old:
                    index = local_names_old.index(localname)
                if action == 'KillAppend':
                    ask_user = True
                    if (index > -1 and local_names_old[:index+1] == local_names_new[:index+1]):
                        action = 'MergeReplace'
                    else:
                        changed_elements.append(self._get_element_diff(new_path_spec, config, extra_verbose))
                        path_changed = True
     
                if action == 'Append':
                    path_changed = True
                    new_elements.append(self._get_element_diff(new_path_spec, config, extra_verbose))
                elif action == 'MergeReplace':
                    changed_elements.append(self._get_element_diff(new_path_spec, config, extra_verbose))
                    ask_user = True
                elif action == 'MergeKeep':
                    discard_elements.append(self._get_element_diff(new_path_spec, config, extra_verbose))
                    ask_user = True
            if len(changed_elements) > 0:
              output += "\n     Change details of element (Use --merge-keep or --merge-replace to change):\n"
              if extra_verbose:
                output += " %s\n"%"\n".join(changed_elements)
              else:
                output += " %s\n"%", ".join(changed_elements)
            if len(new_elements) > 0:
                output += "\n     Add new elements:\n"
                if extra_verbose:
                  output += " %s\n"%"\n".join(new_elements)
                else:
                  output += " %s\n"%", ".join(new_elements)
                
     
            if local_names_old != local_names_new[:len(local_names_old)]:
                old_order = ' '.join(reversed(local_names_old))
                new_order = ' '.join(reversed(local_names_new))
                output += "\n     %s (Use --merge-keep or --merge-replace to prevent) from\n %s\n     to\n %s\n\n"%(path_change_message or "Element Order change", old_order, new_order)
                ask_user = True
     
            if output == "":
                return (None, False)
            if confirmed or not ask_user:
                print("     Performing actions: ")
                print(output)
                return (newconfig, path_changed)
            else:
                print(output)
                showhelp = True
                while(showhelp):
                    showhelp = False
                    prompt = "Continue: (y)es, (n)o, (v)erbosity, (a)dvance options: "
                    mode_input = raw_input(prompt)
                    if mode_input == 'y':
                        return (newconfig, path_changed)
                    elif mode_input == 'n':
                        abort = True
                    elif mode_input == 'a':
                        strategies = {'MergeKeep': "(k)eep",
                                      'MergeReplace': "(s)witch in",
                                      'KillAppend': "(a)ppending"}
                        unselected = [strategies[x] for x in strategies if x != merge_strategy]
                        print( """New entries will just be appended to the config and
appear at the beginning of your ROS_PACKAGE_PATH. The merge strategy
decides how to deal with entries having a duplicate localname or path.

"(k)eep" means the existing entry will stay as it is, the new one will
be discarded. Useful for getting additional elements from other
workspaces without affecting your setup.

"(s)witch in" means that the new entry will replace the old in the
same position. Useful for upgrading/downgrading.

"switch (a)ppend" means that the existing entry will be removed, and
the new entry appended to the end of the list. This maintains order
of elements in the order they were given.

Switch append is the default.
""")
                        prompt = """Change Strategy %s: """%", ".join(unselected)
                        mode_input = raw_input(prompt)
                        if mode_input == 's':
                            merge_strategy = 'MergeReplace'
                        elif mode_input == 'k':
                            merge_strategy = 'MergeKeep'
                        elif mode_input == 'a':
                            merge_strategy = 'KillAppend'
                        
                    elif mode_input == 'v':
                      extra_verbose = not extra_verbose
            if abort:
                print("No changes made.")
                return (None, False)
            print('==========================================')
          
