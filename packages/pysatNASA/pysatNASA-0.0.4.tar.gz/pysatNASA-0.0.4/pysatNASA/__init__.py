"""Core library for pysatNASA.

This is a library of `pysat` instrument modules and methods designed to support
NASA instruments and missions archived at the Community Data Analysis Web
portal.

"""

import os
from pysatNASA import constellations  # noqa F401
from pysatNASA import instruments  # noqa F401

# set version
here = os.path.abspath(os.path.dirname(__file__))
version_filename = os.path.join(here, 'version.txt')
with open(version_filename, 'r') as version_file:
    __version__ = version_file.read().strip()
del here, version_filename, version_file
