#!/usr/bin/env python
from pepper_actuators.pepper_people_follow import PepperPeopleFollow
import qi
import sys
import rospy
if __name__ == "__main__":
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + "192.168.0.164" + ":" + str(9559)
        app = qi.Application(["PepperPeoplePerception", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi.")
        sys.exit(1)

    rospy.init_node('pepper_security_distance', anonymous=True)
    ORTHO_DIST = rospy.get_param('~orth_dist')
    TANGENT_DIST = rospy.get_param('~tang_dist')

    app.start()
    motion = app.session.service("ALMotion")
    motion.setOrthogonalSecurityDistance(ORTHO_DIST)
    motion.setTangentialSecurityDistance(TANGENT_DIST)

