__author__ = 'Florian Lier [flier@techfak.uni-bielefeld.de]'

import rospy
import time
from naoqi_bridge_msgs.msg import JointAnglesWithSpeed
from geometry_msgs.msg import Twist

is_driving = time.time()
max_yaw = 1.5708
min_yaw = -1.5708


def force_driving_pose():
    global is_driving, min_yaw, max_yaw
    rospy.init_node('pepper_force_driving_pose', anonymous=True)
    pub = rospy.Publisher('/pepper_robot/pose/joint_angles', JointAnglesWithSpeed, queue_size=10)
    rate = rospy.Rate(10)
    is_driving = time.time()

    def goal_cb(Twist):
        global is_driving
        if is_driving < time.time():
            angles = JointAnglesWithSpeed()
            angles.joint_names = ['RShoulderRoll',
                                  'RShoulderPitch',
                                  'LShoulderPitch',
                                  'LShoulderRoll',
                                  'HeadPitch',
                                  'HeadYaw']
            # RADIANS
            angles.joint_angles = [0.0, 1.39626, 1.39626, 0.0, 0.261799, 0.0]
            angles.speed = 0.1
            angles.relative = 0
            pub.publish(angles)
            is_driving = time.time()

    goal_sub = rospy.Subscriber('/cmd_vel', Twist, goal_cb)

    while not rospy.is_shutdown():
        rate.sleep()


if __name__ == '__main__':
    try:
        force_driving_pose()
    except rospy.ROSInterruptException:
        pass
