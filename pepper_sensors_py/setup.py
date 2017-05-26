#!/usr/bin/env python
from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    scripts=['nodes/camera.py',
             'nodes/laser.py',
             'nodes/people_perception.py',
             'nodes/position.py',
             'nodes/pepper_speechrec.py'],
    packages=['pepper_sensors'],
    package_dir={'': 'src'}
)

setup(**d)
