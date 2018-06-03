#!/usr/bin/env python
# Author: kkonen - kkonen@techfak.uni-bielefeld.de
import rospy
from people_msgs.msg import People, Person
from geometry_msgs.msg import PointStamped
from visualization_msgs.msg import Marker  # should be implemented for rviz debugging visualization help stuff
from std_msgs.msg import String
import tf
import uuid
import operator

class PepperPeoplePerception(object):
    def __init__(self, app):

        # app and session init
        super(PepperPeoplePerception, self).__init__()
        app.start()
        session = app.session

        # NAOQI SERVICE STUFF
        self.memory = session.service("ALMemory")
        self.peoplesubscriber = self.memory.subscriber("PeoplePerception/PeopleDetected")
        #self.wavesubscriber = self.memory.subscriber("WavingDetection/Waving")
        self.facesubscriber = self.memory.subscriber("FaceCharacteristics/PersonSmiling")

        self.faceConnection = self.facesubscriber.signal.connect(self.onPersonSmiling)
        self.peopleConnection = self.peoplesubscriber.signal.connect(self.onPeopleDetected)
        #self.waveConnection = self.wavesubscriber.signal.connect(self.onWaveDetected)

        self.face_characteristics = session.service("ALFaceCharacteristics")
        #self.movement_detection = session.service("ALMovementDetection")
        self.people_detection = session.service("ALPeoplePerception")
        #self.waving_detection = session.service("ALWavingDetection")
        self.people_detection.subscribe("PepperPeoplePerception")
        #self.waving_detection.subscribe("PepperPeoplePerception")
        self.face_characteristics.subscribe("PepperPeoplePerception")

        self.people_data = []

        self.numPersons = 1

        self.SMILETHRESHOLD = 0.5
        self.EXPRESSIONTHRESHOLD = 0.5



        # ROS
        self.pubPeople = rospy.Publisher("/people_tracker/people", People, queue_size=5)
        #self.pubWaves = rospy.Publisher("/HandCreate", PointStamped, queue_size=5)
        self.pubSmile = rospy.Publisher("/pepper/people_smile", String, queue_size=5)
        self.pubExpression = rospy.Publisher("/pepper/people_expression", String, queue_size=5)
        self.pubShirtColor = rospy.Publisher("/pepper/people_shirt_color", String, queue_size=5)

        rospy.init_node('people_perception', anonymous=True)
        self.rate = rospy.Rate(10)
        self.listener = tf.TransformListener()
        self.startuptime = rospy.Time.now()

    def onPersonSmiling(self, value):
        pass

    #def onWaveDetected(self, value):
    #    print "wave detected"

    def sendMessage(self, string, publisher):
        message = String()
        message.data = string
        publisher.publish(message)

    def onPeopleDetected(self, value):
        persons = value[1]
        print "________________________________________"
        print "\n I see %d people:" % len(persons)
        self.people_data = []
        for it_person in persons:
            key_root = "PeoplePerception/Person/" + str(it_person[0])
            keys = [key_root + "/ShirtColor", key_root + "/PositionInTorsoFrame", key_root + "/RealHeight", key_root + "/SmileProperties", key_root + "/ExpressionProperties",
                    key_root + "/AgeProperties"]
            # keys = [key_root + "/SmileProperties" , key_root + "/ExpressionProperties", key_root + "/AgeProperties"]

            data = self.memory.getListData(keys)
            person_data = [data[1], data[2], data[0], it_person[0]]
            self.people_data.append(person_data)
            self.sendMessage(data[0], self.pubShirtColor)
            print "Smile Level"
            print data[3]
            if len(persons) == 1:
                if data[3] is not None and len(data[3]) > 0:
                    if data[3][0] >= self.SMILETHRESHOLD:
                        self.sendMessage("smiling", self.pubSmile)
            print "Neutral, Happy, Suprised, Angry, Sad"
            print data[4]
            if len(persons) == 1:
                if data[4] is not None and len(data[4]) > 0:
                    index, value = max(enumerate(data[4]), key=operator.itemgetter(1))
                    if value >= self.EXPRESSIONTHRESHOLD:
                        if index == 0:
                            self.sendMessage("neutral", self.pubExpression)
                        if index == 1:
                            self.sendMessage("happy", self.pubExpression)
                        if index == 2:
                            self.sendMessage("surprised", self.pubExpression)
                        if index == 3:
                            self.sendMessage("angry", self.pubExpression)
                        if index == 4:
                            self.sendMessage("sad", self.pubExpression)
            print "Age guess and confidence"
            print data[5]

    def run(self):
        try:
            self.listener.waitForTransform("/torso", "/map", rospy.Time.now(), rospy.Duration(4.0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException, tf.Exception):
            print "Could not find transformation!"
        while not rospy.is_shutdown():
            now = rospy.Time.now()
            # GETTING THE TRANSFORMATION FROM PEPPER TORSO FRAME TO MAP FRAME
            try:
                self.listener.waitForTransform("/torso", "/map", now, rospy.Duration(4.0))
                (trans, rot) = self.listener.lookupTransform('/torso', '/map', now)
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException, tf.Exception):
                print "Could not find transformation!"

            # waving = HandCreate()
            people = People()
            persons = []
            point = PointStamped()
            point.header.frame_id = "/torso"
            point.header.stamp = now
            for it_person in self.people_data:
                person = Person()
                uuidseed = str(self.startuptime) + str(it_person[3])
                person.name = str(uuid.uuid5(uuid.NAMESPACE_DNS, uuidseed))
                point.point.x = it_person[0][0]
                point.point.y = it_person[0][1]
                point.point.z = it_person[0][2]
                try:
                    person.position = self.listener.transformPoint("/map", point).point
                except (tf.LookupException, tf.ExtrapolationException):
                    print "Transform not available!"
                #if it_person[4] == 1:
                #    self.pubWaves(person.position)

                persons.append(person)

            self.people_data = []
            people.header.stamp = rospy.Time.now()
            people.header.frame_id = "/map"
            people.people = persons
            if len(persons) >= self.numPersons:
                self.pubPeople.publish(people)
            self.rate.sleep()

        # DISCONNECTING SIGNALS AND UNSUBSCRIBING SUBSCRIBERS
        #self.waving_detection.unsubscribe("PepperPeoplePerception")
        #self.wavesubscriber.signal.disconnect(self.waveConnection)
        self.people_detection.unsubscribe("PepperPeoplePerception")
        self.peoplesubscriber.signal.disconnect(self.peopleConnection)
        self.face_characteristics.unsubscribe("PepperPeoplePerception")
        self.facesubscriber.signal.disconnect(self.faceConnection)
        print "Unsubscribed all services"
