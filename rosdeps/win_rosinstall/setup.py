
from distutils.core import setup


setup(name='rosinstall',
      version= '0.6.18',
      packages=['rosinstall', 'vcstools'],
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
      description = "Windows implementation of the installer for ROS", 
      long_description = """\
Checks out repos from a .rosinstall description
""",
      license = "BSD"
      )
