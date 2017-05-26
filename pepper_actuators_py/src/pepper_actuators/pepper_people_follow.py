#!/usr/bin/env python
# Author: kkonen - kkonen@techfak.uni-bielefeld.de
import rospy
import time
import signal
from std_msgs.msg import String



# could be rewritten to be an tracking actuator which can track faces people bodys redballs
# and trackingmodes like following/headtracking

class PepperPeopleFollow(object):
    def __init__(self, app):

        # app and session init
        super(PepperPeopleFollow, self).__init__()
        app.start()
        session = app.session

        rospy.init_node('pepper_people_follow', anonymous=True)
        self.rate = rospy.Rate(10)
        self.memory = session.service("ALMemory")
        self.motion = session.service("ALMotion")
        self.people_detection = session.service("ALPeoplePerception")
        self.subscriber = self.memory.subscriber("PeoplePerception/PeopleDetected")
        self.people_detection.subscribe("PepperPeopleFollow")

        self.tracker_service = session.service("ALTracker")
        self.personId = []
        self.follow = False

        self.subPose = rospy.Subscriber("/startfollow", String, self.onStartFollowCommand)
        self.subPose2 = rospy.Subscriber("/stopfollow", String, self.onStopFollowCommand)
        self.peopleConnect = self.subscriber.signal.connect(self.onPeopleDetected)

    def onPeopleDetected(self, value):
        self.personId = value[1][0][0]

    def onStartFollowCommand(self, value):
        print "called start"
        print value
        self.follow = True

    def onStopFollowCommand(self, value):
        print "called stop"
        print value
        self.follow = False

    def run(self):
        try:
            signal.signal(signal.SIGINT, signal.default_int_handler)
            if not self.motion.robotIsWakeUp():
                self.motion.wakeUp()
                print "woke up"
            while not rospy.is_shutdown():
                self.rate.sleep()
                time.sleep(5)
                while self.follow is False:
                    pass
                print "follow true"
                while self.personId == []:
                    pass

                print "following will start now"
                self.tracker_service.registerTarget("People", self.personId)
                self.tracker_service.setMode("Navigate")
                self.tracker_service.track("People")

                print "We are now following a person!"

                while self.follow is True:
                    time.sleep(1)

                # Stop tracker.
                self.tracker_service.stopTracker()
                self.tracker_service.unregisterAllTargets()
                print "ALTracker stopped."
                self.personId = []
        except KeyboardInterrupt:
            print "shutting down!"
            self.people_detection.unsubscribe("PepperPeopleFollow")
            self.subscriber.signal.disconnect(self.peopleConnect)
            print "disconnected"
            exit(0)

        self.people_detection.unsubscribe("PepperPeopleFollow")
        self.subscriber.signal.disconnect(self.peopleConnect)
        print "disconnected"
