#!/usr/bin/env python
from pepper_actuators.pepper_move_to import PepperMoveTo
import qi
import sys

if __name__ == "__main__":

    try:
        # Initialize qi framework.
        connection_url = "tcp://" + "192.168.0.164" + ":" + str(9559)
        app = qi.Application(["PepperPeoplePerception", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect ")
        sys.exit(1)

    pepperMoveTo = PepperMoveTo(app)
    pepperMoveTo.run()
