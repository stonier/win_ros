
from distutils.core import setup


setup(name='rosinstall',
      version= '0.1.0',
      packages=['rosinstall', 'vcstools', 'wstool'],
      package_dir = {'':'src'},
      scripts = ["scripts/win-rosinstall.py", "scripts/rosinstall.bat", "scripts/win-rosws.py", "scripts/rosws.bat", "scripts/win-rosinstall-setupfiles.py"],
      author = "Daniel Stonier", 
      author_email = "d.stonier@gmail.com",
      url = "https://github.com/stonier/win_ros/",
      download_url = "http://files.yujinrobot.com/appupdater/python/2.7/", 
      keywords = ["ROS"],
      classifiers = [
        "Programming Language :: Python", 
        "License :: OSI Approved :: BSD License" ],
      description = "Pythong tools for a win_ros build environment", 
      long_description = """\
Python tools for managing a win_ros build environment (vcstools, rosinstall, wstool, rospkg.
""",
      license = "BSD"
      )
