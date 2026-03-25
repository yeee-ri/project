#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Header
from geometry_msgs.msg import Pose

class project():
    def __init__(self):
        rospy.init_node('controller',anonymous = True)
        self.pub = rospy.Publisher('/move_base_simple/goal',PoseStamped, queue_size = 10)

    def move_to(self):
        data = [0.833, -0.721, 0.0, 0.0, 0.0, -0.04, 1.0]
        
        Pose = PoseStamped()
        Pose.header.stamp = rospy.Time.now()
        Pose.header.frame_id = 'map'

        Pose.pose.position.x = data[0]
        Pose.pose.position.y = data[1]
        Pose.pose.position.z = data[2]
        Pose.pose.orientation.x = data[3]
        Pose.pose.orientation.y = data[4]
        Pose.pose.orientation.z = data[5]
        Pose.pose.orientation.w = data[6]

        self.pub.publish(Pose)


if __name__ == '__main__':
    controller = project()
    rospy.sleep(1.0)
    controller.move_to()
    rospy.spin() 



