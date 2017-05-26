#!/usr/bin/env python
# Author: kkonen - kkonen@techfak.uni-bielefeld.de
import rospy

from std_msgs.msg import String


class PepperAnimationPlayer(object):
    def __init__(self, app):
        # app and session init
        super(PepperAnimationPlayer, self).__init__()
        app.start()
        session = app.session

        # NAOQI SERVICE STUFF

        rospy.init_node('pepper_animation_player', anonymous=True)

        self.memory = session.service("ALMemory")
        self.animation_player = session.service("ALAnimationPlayer")
        self.subAnimation = rospy.Subscriber("/pepper/animation_player", String, self.callbackAnimation)

    def callbackAnimation(self, string):
        print string
        self.animation_player.run(string.data)

    def run(self):
        while not rospy.is_shutdown():
            pass
        self.animation_player.reset()

# Link to animations
# http://doc.aldebaran.com/2-5/naoqi/motion/alanimationplayer-advanced.html#animationplayer-list-behaviors-pepper
# DEFAULT POSE: animations/Stand/Gestures/Nothing_1
# CALM DOWN (ANGRY REACTION) : animations/Stand/Gestures/CalmDown_3
# HAPPY REACTION: animations/Stand/Emotions/Positive/Happy_1
# NEUTRAL REACTION: animations/Stand/Gestures/YouKnowWhat_1
# SAD REACTION: animations/Stand/Emotions/Positive/Peaceful_1
# SURPRISED REACTION: animations/Stand/Gestures/Enthusiastic_4
# WAVING POSE: animations/Stand/Gestures/Hey_1
