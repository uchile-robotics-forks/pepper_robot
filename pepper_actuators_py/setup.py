#!/usr/bin/env python
from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    scripts=['nodes/naoqi_tts.py', 'nodes/people_follow.py', 'nodes/move_to.py', 'nodes/force_driving_pose.py', 'nodes/wakeup.py',
             'nodes/animation_player.py', 'nodes/security_distance.py'],
    packages=['pepper_actuators'],
    package_dir={'': 'src'}
)

setup(**d)
