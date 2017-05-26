#!/usr/bin/env python
import rospy
from std_msgs.msg import String
# import NAO dependencies
from naoqi_driver.naoqi_node import NaoqiNode
import time

from pepper_sensors.vocabulary import *


class SpeechRec(object):
    def __init__(self, app, confidenceThreshold=0.4, pathToBNFs=[]):
        """
        
        :param app: 
        :param confidenceThreshold: sets a threshold for the confidence of a understood sentences. Sentences with a lower threshold will not be published.
        :param pathToJSGFs: The path to the jsgf file which contains the grammar.
        """
        self.confidenceThreshold = confidenceThreshold

        super(SpeechRec, self).__init__()
        app.start()
        session = app.session

        # Defaults
        self.EVENT = "WordRecognized"
        self.NODE_NAME = "pepper_speech"
        self.rec = None
        self.sig = None
        self.vocabulary = None
        self.pubs = {}
        """publishers
        """

        # generate vocabulary
        generateVocabularies(pathToBNFs)
        self.vocabulary = []
        for scope in voc:
            self.vocabulary.extend(voc[scope])

        # NAOQI SERVICE STUFF
        self.memory = session.service("ALMemory")
        self.mem_subscriber = self.memory.subscriber(self.EVENT)
        self.sig = self.mem_subscriber.signal.connect(self.on_word_recognised)
        self.rec = session.service("ALSpeechRecognition")
        self.rec.pause(True)
        self.rec.setAudioExpression(False)
        self.rec.setVisualExpression(False)
        #self.rec.setVocabulary(self.vocabulary, True) # True/ False for wordspotting, meaning should pepper hear for words even if they are embedded in utterance [further tests to determine usefullness needed]
        self.rec.compile('/home/salt/speechrec-stuff/grammar.bnf', '/home/salt/speechrec-stuff/grammar.lcf', 'English')
        self.rec.addContext('/home/nao/grammar.lcf', 'confirm')
        self.rec.pause(False)
        self.rec.subscribe(self.NODE_NAME)

        #set the confirmgrammar to publisher
        self.pubs['confirm'] = rospy.Publisher("/pepper/speechrec/confirm", String, queue_size=5)

        # set each context(/listened after nonterminal) as publisher
        for context in voc:
            # by adding a new generic attribute in this class which is
            self.pubs[context] = rospy.Publisher("/pepper/speechrec/" + context, String, queue_size=5)
        rospy.init_node('pepper_speech_rec', anonymous=True)

        print("SpeechRec Node Configured")

    def on_word_recognised(self, value):
        """Publish the words recognized by NAO via ROS """
        result = value[0]
        rospy.loginfo("Well, all I heard was: %s " % result)
        rospy.loginfo("confidence: " + str(value[1]))
        rospy.loginfo("complete list : " + str(value))
        # check for confidence
        if value[1] > self.confidenceThreshold:
            # check for grammar
            if "yes" in result or "no" in result:
                self.pubs['confirm'].publish(result)
            else:
                for context in voc:
                    if result in voc[context]:
                        self.pubs[context].publish(result)

    def on_word_recognized_and_grammar(self, value):
        self.on_word_recognised(value)

    def run(self):
        while not rospy.is_shutdown():
            time.sleep(0.5)
        self.rec.unsubscribe(self.NODE_NAME)
        self.mem_subscriber.signal.disconnect(self.sig)
