#!/usr/bin/env python
import rospy
from pepper_sensors.pepper_speechrec import SpeechRec
from naoqi import ALProxy
import qi
import sys

if __name__ == "__main__":
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + "192.168.0.164" + ":" + str(9559)
        app = qi.Application(["SpeechRec", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n" "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    pepper_speech_rec = SpeechRec(app)
    pepper_speech_rec.run()
