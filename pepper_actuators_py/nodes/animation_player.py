#!/usr/bin/env python
from pepper_actuators.pepper_animation_player import PepperAnimationPlayer
import qi
import sys

if __name__ == "__main__":
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + "192.168.0.164" + ":" + str(9559)
        app = qi.Application(["PepperAnimationPlayer", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi")
        sys.exit(1)

    pepperAnimationPlayer = PepperAnimationPlayer(app)
    pepperAnimationPlayer.run()
