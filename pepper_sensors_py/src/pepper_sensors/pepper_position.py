#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped, Pose
from nav_msgs.msg import Odometry
import tf


class PepperPosition(object):
    def __init__(self, app):
        # app and session init
        super(PepperPosition, self).__init__()
        app.start()
        session = app.session
        # ROS
        self.poseC = PoseWithCovarianceStamped()
        rospy.init_node('pepper_position', anonymous=True)
        self.rate = rospy.Rate(10)
        self.poseS = PoseStamped()
        self.poseS.header.frame_id = "/map"
        self.pose = Pose()
        self.listener = tf.TransformListener()
        self.now = rospy.Time()
        self.subPose = rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, self.callbackPose)
        self.pub = rospy.Publisher("/pepper/pose", Odometry, queue_size=10)

    def callbackPose(self, data):
        self.now = rospy.Time()
        self.poseC = data
        self.listener.waitForTransform("/map", "/odom", self.now, rospy.Duration(4.0))
        (trans, rot) = self.listener.lookupTransform('/map', '/odom', self.now)
        self.poseS.pose = self.poseC.pose.pose
        self.pose = self.listener.transformPose("/odom", self.poseS).pose

    def run(self):
        global mutex
        while not rospy.is_shutdown():
            odom = Odometry()
            odom.header.stamp = self.now
            odom.child_frame_id = "/odom"
            odom.pose.pose = self.pose
            self.pub.publish(odom)
            self.rate.sleep()
