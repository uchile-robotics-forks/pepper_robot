#!/usr/bin/env python
import rospy
from std_msgs.msg import String


class PepperWakeUp(object):
    def __init__(self, app):

        # app and session init
        super(PepperWakeUp, self).__init__()
        app.start()
        session = app.session
        rospy.init_node('pepper_wakeup', anonymous=True)
        self.rate = rospy.Rate(10)
        self.motion = session.service("ALMotion")

        self.sub_wake = rospy.Subscriber("/wake", String, self.onWakeUp)
        self.sub_rest = rospy.Subscriber("/rest", String, self.onRest)

    def onWakeUp(self, value):

        # check if robot is already woken up
        if self.motion.robotIsWakeUp():
            print 'doing nothing as robot is already awake'
            return

        self.motion.wakeUp()
        print 'robot woken up'

    def onRest(self, value):

        self.motion.rest()
        print 'put robot to rest'

    def run(self):
        while not rospy.is_shutdown():
            pass
