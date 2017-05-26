#!/usr/bin/env python
import rospy
from pepper_actuators.naoqi_tts import TTS

if __name__ == "__main__":
  tts = TTS()

  rospy.spin()
  exit(0)


