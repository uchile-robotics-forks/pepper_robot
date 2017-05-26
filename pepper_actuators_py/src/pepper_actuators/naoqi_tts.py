#!/usr/bin/env python
import rospy
from std_msgs.msg import String

# import NAO dependencies
from naoqi_driver.naoqi_node import NaoqiNode


class TTS(NaoqiNode):
    def __init__(self):
        NaoqiNode.__init__(self, 'naoqi_tts')
        self.connectNaoQi()
        rospy.Subscriber("talk", String, self.sayMessage)

    # (re-) connect to NaoQI:
    def connectNaoQi(self):
        '''Connect to Naoqi modules
        '''
        rospy.loginfo("TTS Node Connecting to NaoQi at %s:%d", self.pip, self.pport)

        # version check
        version_array = self.get_proxy("ALSystem").systemVersion().split('.')
        if len(version_array) < 3:
            rospy.logerr("Unable to deduce the system version.")
            exit(0)
        version_tuple = (int(version_array[0]), int(version_array[1]), int(version_array[2]))
        min_version = (2, 5, 2)
        if version_tuple < min_version:
            rospy.logerr("Naoqi version " + str(min_version) +
                         " required for localization. Yours is " + str(version_tuple))
            exit(0)

        self.tts = self.get_proxy("ALTextToSpeech")

    def sayMessage(self, saystring):
        print 'got data'
        self.tts.say(saystring.data)
        print 'return'
