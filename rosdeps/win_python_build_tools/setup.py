
from distutils.core import setup


setup(name='winros-python-build-tools',
      version= '0.1.0',
      packages=['rosinstall', 'vcstools', 'wstool', 'rospkg', 'catkin_pkg', 'win_ros'],
      package_dir = {'':'src'},
      scripts = ["scripts/winros_wstool.py", "scripts/wstool.bat",
                 "scripts/winros_rosversion.py", "scripts/rosversion.bat", 
                 "scripts/winros_catkin_create_pkg.py", "scripts/catkin_create_pkg.bat", 
                 "scripts/winros_init_workspace.py", "scripts/winros_init_workspace.bat"],
      author = "Daniel Stonier", 
      author_email = "d.stonier@gmail.com",
      url = "https://github.com/stonier/win_python_build_tools",
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
