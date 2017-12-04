import sys
from cx_Freeze import setup, Executable

# graphName = sys.argv[1]
# algo = sys.argv[2]
# cutoff = sys.argv[3]
# seed = sys.argv[4]

setup(
    name = "Any Name",
    version = "3.1",
    description = "Any Description you like",
    executables = [Executable("test.py", base = None)])
# from distutils.core import setup
# import py2exe

# setup(console=['test.py'])