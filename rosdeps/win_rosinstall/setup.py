
from distutils.core import setup


setup(name='win_rosinstall',
      version= '0.6.17',
      packages=['rosinstall', 'vcstools'],
      package_dir = {'':'src'},
      scripts = ["scripts/win-rosinstall.py", "scripts/win-rosinstall.bat", "scripts/win-setupfiles.py"],
      author = "Daniel Stonier", 
      author_email = "d.stonier@gmail.com",
      url = "http://code.google.com/p/win-ros-pkg/wiki/WinRosinstall",
      download_url = "http://code.google.com/p/win-ros-pkg/downloads/list", 
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
