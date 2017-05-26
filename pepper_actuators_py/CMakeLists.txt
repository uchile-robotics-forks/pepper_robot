cmake_minimum_required(VERSION 2.8.3)
project(pepper_actuators_py)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin)

## Uncomment this if the package has a setup.py. This macro ensures
## modules and global scripts declared therein get installed
## See http://ros.org/doc/api/catkin/html/user_guide/setup_dot_py.html
catkin_python_setup()

###################################
## catkin specific configuration ##
###################################
catkin_package()


#############
## Install ##
#############

catkin_install_python(PROGRAMS nodes/naoqi_tts.py nodes/people_follow.py nodes/move_to.py
                               nodes/force_driving_pose.py nodes/wakeup.py nodes/animation_player.py nodes/security_distance.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

## Mark cpp header files for installation
install(DIRECTORY launch
   DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
   FILES_MATCHING PATTERN "*.launch"
)

