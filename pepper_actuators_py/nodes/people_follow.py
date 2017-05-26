#!/usr/bin/env python
from pepper_actuators.pepper_people_follow import PepperPeopleFollow
import qi
import sys

if __name__ == "__main__":
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + "192.168.0.164" + ":" + str(9559)
        app = qi.Application(["PepperPeoplePerception", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + " Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    pepperFollow = PepperPeopleFollow(app)
    pepperFollow.run()
