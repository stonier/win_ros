
from distutils.core import setup


setup(name='winros-python-build-tools',
      version= '0.1.0',
      packages=['rosinstall', 'vcstools', 'wstool', 'rospkg'],
      package_dir = {'':'src'},
      scripts = ["scripts/win-wstool.py", "scripts/wstool.bat",
                 "scripts/win-rosversion.py", "scripts/rosversion.bat", 
                 "scripts/win-wstool-setupfiles.py"],
      author = "Daniel Stonier", 
      author_email = "d.stonier@gmail.com",
      url = "https://github.com/stonier/win_ros/",
      download_url = "http://files.yujinrobot.com/windows/python/2.7/", 
      keywords = ["ROS"],
      classifiers = [
        "Programming Language :: Python", 
        "License :: OSI Approved :: BSD License" ],
      description = "Python tools for a win_ros build environment", 
      long_description = """\
Python tools for managing a win_ros build environment (vcstools, rosinstall, wstool, rospkg.
""",
      license = "BSD"
      )
