#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Vector3


class PepperMoveTo(object):
    def __init__(self, app):

        # SOMETHING
        super(PepperMoveTo, self).__init__()
        app.start()
        session = app.session

        rospy.init_node('pepper_move_to', anonymous=True)
        self.sub = rospy.Subscriber("/pepper/driveGoal", Vector3, self.onDriveGoal)
        print "Subscribed and ready to publish"
        self.rate = rospy.Rate(10)
        # Get the services ALMemory and ALMotion
        self.motion = session.service("ALMotion")
        self.memory = session.service("ALMemory")
        self.subscriber = self.memory.subscriber("ALMotion/MoveFailed")
        self.subscriber.signal.connect(self.onMoveFailed)

    def onMoveFailed(self, data):
        print data
        self.cause = data[1]

    def onDriveGoal(self, data):
        print "Moving Pepper"
        print data
        self.motion.moveTo(data.x, data.y, data.z)

    def run(self):
        self.motion.wakeUp()
        print "waiting for Moves"
        while not rospy.is_shutdown():
            self.rate.sleep()
