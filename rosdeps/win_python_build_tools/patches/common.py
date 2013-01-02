# Software License Agreement (BSD License)
#
# Copyright (c) 2009, Willow Garage, Inc.
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
import copy
# choosing multiprocessing over threading for clean Control-C interrupts (provides terminate())
from urlparse import urlparse
from multiprocessing import Process, Manager
from vcstools.vcs_base import VcsError

class MultiProjectException(Exception): pass

def samefile(f1, f2):
    "Test whether two pathnames reference the same actual file"
    try:
        return os.path.samefile(f1,f2)
    except AttributeError:
        try:
            from nt import _getfinalpathname
            return _getfinalpathname(f1) == _getfinalpathname(f2)
        except (NotImplementedError, ImportError):
            # On Windows XP and earlier, two files are the same if their
            #  absolute pathnames are the same.
            # Also, on other operating systems, fake this method with a
            #  Windows-XP approximation.
            return os.path.abspath(f1) == os.path.abspath(f2)

def conditional_abspath(uri):
  """
  @param uri: The uri to check
  @return: abspath(uri) if local path otherwise pass through uri
  """
  u = urlparse(uri)
  if u.scheme == '': # maybe it's a local file?
    return os.path.abspath(uri)
  else:
    return uri

def is_web_uri(source_uri):
  if source_uri is None or source_uri == '':
    return False
  parsed_uri = urlparse(source_uri)
  if (parsed_uri.scheme == ''
      and parsed_uri.netloc == ''
      and not '@' in parsed_uri.path.split('/')[0]):
    return False
  return True

def normabspath(localname, path):
  """
  if localname is absolute, return it normalized. If relative, return normalized join of path and localname
  """
  if os.path.isabs(localname) or path is None:
    return os.path.realpath(localname)
  abs_path = os.path.realpath(os.path.join(path, localname))
  return abs_path

def realpath_relation(abspath1, abspath2):
  """
  Computes the relationship abspath1 to abspath2
  :returns: None, 'SAME_AS', 'PARENT_OF', 'CHILD_OF'
  """
  assert os.path.isabs(abspath1)
  assert os.path.isabs(abspath2)
  realpath1 = os.path.realpath(abspath1)
  realpath2 = os.path.realpath(abspath2)
  if os.path.dirname(realpath1) == os.path.dirname(realpath2):
    if os.path.basename(realpath1) == os.path.basename(realpath2):
      return 'SAME_AS'
    return None
  else:
    commonprefix = os.path.commonprefix([realpath1, realpath2])
    if commonprefix == realpath1:
      return 'PARENT_OF'
    elif commonprefix == realpath2:
      return 'CHILD_OF'
  return None

def select_element(elements, localname):
  """
  selects entry among elements where path or localname matches.
  Prefers localname matches in case of ambiguity.
  """
  path_candidate = None
  if localname is not None:
    realpath = os.path.realpath(localname)
    for element in elements:
      if localname == element.get_local_name():
        path_candidate = element
        break
      elif realpath == os.path.realpath(element.get_path()):
        path_candidate = element
  return path_candidate


def select_elements(config, localnames):
  """
  selects config elements with given localnames, returns in the order given in config
  If localnames has one element which is path of the config, return all elements
  """
  if config is None:
    return []
  if localnames is None:
    return config.get_config_elements()
  elements = config.get_config_elements()
  selected = []
  notfound = []
  for localname in localnames:
    element = select_element(elements, localname)
    if element is not None:
      selected.append(element)
    else:
      notfound.append(localname)
  if notfound != []:
    raise MultiProjectException("Unknown elements '%s'"%notfound)
  result = []
  # select in order and remove duplicates
  for element in config.get_config_elements():
    if element in selected:
      result.append(element)
  if result == []:
      if (len(localnames) == 1
          and os.path.realpath(localnames[0]) == os.path.realpath(config.get_base_path())):
        return config.get_elements()
  return result
  
  
## Multithreading The following classes help with distributing work
## over several instances, providing wrapping for starting, joining,
## collecting results, and catching Exceptions. Also they provide
## support for running groups of threads sequentially, for the case
## that some library is not thread-safe.
  
class WorkerThread(Process):

  def __init__(self, worker, outlist, index):
    Process.__init__(self)
    self.worker = worker
    if worker is None or worker.element is None:
      raise MultiProjectException("Bug: Invalid Worker")
    self.outlist = outlist
    self.index = index

  def run(self):
    result = {}
    try:
      result = {'entry': self.worker.element.get_path_spec()}
      result_dict = self.worker.do_work()
      if result_dict is not None:
        result.update(result_dict)
      else:
        result.update({'error': MultiProjectException("worker returned None")})
    except MultiProjectException as e:
      result.update({'error': e})
    except VcsError as e:
      result.update({'error': e})
    except OSError as e:
      result.update({'error': e})
    except Exception as e:
      # this would be a bug, and we need trace to find them in multithreaded cases.
      import sys, traceback
      traceback.print_exc(file=sys.stderr)
      result.update({'error': e})
    self.outlist[self.index] = result

class DistributedWork():
  
  def __init__(self, capacity, num_threads=10, silent=True):
    man = Manager() # need managed array since we need the results later
    self.outputs = man.list([None for _ in range(capacity)])
    self.threads = []
    self.sequentializers = {}
    self.index = 0
    self.num_threads = num_threads
    self.silent = silent
    
  def add_thread(self, worker):
    thread = WorkerThread(worker, self.outputs, self.index)
    if self.index >= len(self.outputs):
      raise MultiProjectException("Bug: Declared capacity exceeded %s >= %s"%(self.index, len(self.outputs)))
    self.index += 1
    self.threads.append(thread)
    
  # def add_to_sequential_thread_group(self, worker, group):
  #   """Workers in each sequential thread group run one after the other, groups run in parallel"""
  #   class ThreadSequentializer(Process):
  #     """helper class to run 'threads' one after the other"""
  #     def __init__(self):
  #       Process.__init__(self)
  #       self.workers = []
  #     def add_worker(self, worker):
  #       self.workers.append(worker)
  #     def run(self):
  #     for worker in self.workers:
  #       worker.run() # not calling start on purpose
  #   thread = WorkerThread(worker, self.outputs, self.index)
  #   if self.index >= len(self.outputs):
  #     raise MultiProjectException("Bug: Declared capacity exceeded %s >= %s"%(self.index, len(self.outputs)))
  #   self.index += 1
  #   if group not in self.sequentializers:
  #     self.sequentializers[group] = ThreadSequentializer()
  #     self.sequentializers[group].add_worker(thread)
  #     self.threads.append(self.sequentializers[group])
  #   else:
  #     self.sequentializers[group].add_worker(thread)
    
  def run(self):
    """
    Execute all collected workers, terminate all on KeyboardInterrupt
    """
    if self.threads == []:
      return []
    if (self.num_threads == 1):
      for thread in self.threads:
        thread.run()
    else:
      # The following code is rather delicate and may behave differently
      # using threading or multiprocessing. running_threads is
      # intentionally not used as a shrinking list because of al the
      # possible multithreading / interruption corner cases
      # Not using Pool because of KeyboardInterrupt cases
      try:
        waiting_index = 0
        maxthreads = self.num_threads
        running_threads = []
        missing_threads = copy.copy(self.threads)
        # we are done if all threads have finished
        while len(missing_threads) > 0:
          # we spawn more threads whenever some threads have finished
          if len(running_threads) < maxthreads:
            to_index = min(waiting_index + maxthreads - len(running_threads), len(self.threads))
            for i in range(waiting_index, to_index):
              self.threads[i].start()
              running_threads.append(self.threads[i])
            waiting_index = to_index
          # threads have exitcode only once they terminated
          missing_threads = [t for t in missing_threads if t.exitcode is None]
          running_threads = [t for t in running_threads if t.exitcode is None]
          if (not self.silent
              and len(running_threads) > 0):
            print("[%s] still active"%",".join([th.worker.element.get_local_name() for th in running_threads]))
          for thread in running_threads:
            thread.join(1) # this should prevent busy waiting
      except KeyboardInterrupt as k:
        for thread in self.threads:
          if thread is not None and thread.is_alive():
            print("[%s] terminated while active"%thread.worker.element.get_local_name())
            thread.terminate()
        raise k
    
    self.outputs = filter(lambda x: x is not None, self.outputs)
    message = ''
    for output in self.outputs:
      if "error" in output:
        if 'entry' in output:
          message += "Error processing '%s' : %s\n"%(output['entry'].get_local_name(), output["error"])
        else:
          message += "%s\n"%output["error"]
    if message != '':
      raise MultiProjectException(message)
    return self.outputs
