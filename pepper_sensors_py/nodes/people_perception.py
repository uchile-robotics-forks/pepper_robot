#!/usr/bin/env python
import rospy
from pepper_sensors.pepper_people_perception import PepperPeoplePerception
import qi
import sys

if __name__ == "__main__":
  try:
        # Initialize qi framework.
        connection_url = "tcp://" + "192.168.0.164" + ":" + str(9559)
        app = qi.Application(["PepperPeoplePerception", "--qi-url=" + connection_url])
  except RuntimeError:
      print ("Can't connect to Naoqi")
      sys.exit(1)

  pepperPeople = PepperPeoplePerception(app)
  pepperPeople.run()

