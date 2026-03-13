#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import rospy
import tf2_ros
import tf_conversions
import time

from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from controller import Robot, Keyboard

class WebotsNavController:
    def __init__(self):
        rospy.init_node("webots_nav_controller", anonymous=False)

        self.robot = Robot()
        self.timestep = int(self.robot.getBasicTimeStep())
        self.dt = self.timestep / 1000.0

        self.m1 = self.robot.getDevice("wheel1")
        self.m2 = self.robot.getDevice("wheel2")
        self.m3 = self.robot.getDevice("wheel3")
        self.m4 = self.robot.getDevice("wheel4")

        self.motors = [self.m1, self.m2, self.m3, self.m4]
        for m in self.motors:
            m.setPosition(float('inf'))
            m.setVelocity(0.0)

        self.lidar = self.robot.getDevice("HeadLidar")
        self.lidar.enable(self.timestep)

        self.keyboard = Keyboard()
        self.keyboard.enable(self.timestep)

        self.odom_scale_x = rospy.get_param("~odom_scale_x", 0.30)
        self.odom_scale_y = rospy.get_param("~odom_scale_y", 1.20)
        self.odom_scale_w = rospy.get_param("~odom_scale_w", 0.50)

        self.r = rospy.get_param("~wheel_radius", 0.076)
        self.lx = rospy.get_param("~lx", 0.15)
        self.ly = rospy.get_param("~ly", 0.10)
        self.max_wheel_speed = rospy.get_param("~max_wheel_speed", 8.0)

        self.kx = rospy.get_param("~kx", 6.0)
        self.ky = rospy.get_param("~ky", 6.0)
        self.kz = rospy.get_param("~kz", 3.0)

        self.key_vx = rospy.get_param("~key_vx", 0.3)
        self.key_vy = rospy.get_param("~key_vy", 0.3)
        self.key_wz = rospy.get_param("~key_wz", 0.5)

        self.base_frame = rospy.get_param("~base_frame", "base_link")
        self.odom_frame = rospy.get_param("~odom_frame", "odom")
        self.laser_frame = rospy.get_param("~laser_frame", "laser")

        self.cmd_vx = 0.0
        self.cmd_vy = 0.0
        self.cmd_wz = 0.0

        self.manual_vx = 0.0
        self.manual_vy = 0.0
        self.manual_wz = 0.0

        self.last_ros_cmd_time = rospy.Time(0)
        self.ros_cmd_timeout = rospy.Duration(rospy.get_param("~ros_cmd_timeout", 0.3))
        self.last_key_time = rospy.Time(0)
        self.key_timeout = rospy.Duration(rospy.get_param("~key_timeout", 0.2))

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0

        self.last_odom_time = rospy.Time.now()

        rospy.Subscriber("/cmd_vel", Twist, self.cb_cmd_vel, queue_size=1)
        self.odom_pub = rospy.Publisher("/odom", Odometry, queue_size=20)
        self.scan_pub = rospy.Publisher("/scan", LaserScan, queue_size=20)
        self.tf_br = tf2_ros.TransformBroadcaster()
        self.static_tf_br = tf2_ros.StaticTransformBroadcaster()        
        
        laser_tf = TransformStamped()
        laser_tf.header.stamp = rospy.Time.from_sec(time.time())
        laser_tf.header.frame_id = "base_link"
        laser_tf.child_frame_id = "laser"
        
        laser_tf.transform.translation.x = 0.0
        laser_tf.transform.translation.y = 0.0
        laser_tf.transform.translation.z = 0.155
        
        q = tf_conversions.transformations.quaternion_from_euler(0, 0, 0)
        laser_tf.transform.rotation.x = q[0]
        laser_tf.transform.rotation.y = q[1]
        laser_tf.transform.rotation.z = q[2]
        laser_tf.transform.rotation.w = q[3]
        
        self.static_tf_br.sendTransform(laser_tf)

        print("controller init done")
        print("lidar device:", self.lidar)

    def cb_cmd_vel(self, msg):
        self.cmd_vx = msg.linear.x
        self.cmd_vy = msg.linear.y
        self.cmd_wz = msg.angular.z
        self.last_ros_cmd_time = rospy.Time.from_sec(time.time())

    def drive_ik(self, vx, vy, wz):
        w1 = -self.kx * vx - self.ky * vy - self.kz * wz
        w2 =  self.kx * vx - self.ky * vy - self.kz * wz
        w3 = -self.kx * vx + self.ky * vy - self.kz * wz
        w4 =  self.kx * vx + self.ky * vy - self.kz * wz
        return [w1, w2, w3, w4]
    
    def mecanum_fk(self, w1, w2, w3, w4):
        vx = (-w1 + w2 - w3 + w4) / (4.0 * self.kx)
        vy = (-w1 - w2 + w3 + w4) / (4.0 * self.ky)
        wz = (-w1 - w2 - w3 - w4) / (4.0 * self.kz)

        vx *= self.odom_scale_x
        vy *= self.odom_scale_y
        wz *= self.odom_scale_w

        return vx, vy, wz
    
    def clamp(self, value, min_v, max_v):
        return max(min(value, max_v), min_v)

    def poll_keyboard(self):
        key = self.keyboard.getKey()
        updated = False

        while key != -1:
            if key in (ord('W'), ord('w')):
                self.manual_vx = self.key_vx
                self.manual_vy = 0.0
                self.manual_wz = 0.0
                updated = True
            elif key in (ord('S'), ord('s')):
                self.manual_vx = -self.key_vx
                self.manual_vy = 0.0
                self.manual_wz = 0.0
                updated = True
            elif key in (ord('A'), ord('a')):
                self.manual_vx = 0.0
                self.manual_vy = self.key_vy
                self.manual_wz = 0.0
                updated = True
            elif key in (ord('D'), ord('d')):
                self.manual_vx = 0.0
                self.manual_vy = -self.key_vy
                self.manual_wz = 0.0
                updated = True
            elif key in (ord('Q'), ord('q')):
                self.manual_vx = 0.0
                self.manual_vy = 0.0
                self.manual_wz = self.key_wz
                updated = True
            elif key in (ord('E'), ord('e')):
                self.manual_vx = 0.0
                self.manual_vy = 0.0
                self.manual_wz = -self.key_wz
                updated = True
            elif key == ord(' '):
                self.manual_vx = 0.0
                self.manual_vy = 0.0
                self.manual_wz = 0.0
                updated = True
            key = self.keyboard.getKey()

        if updated:
            self.last_key_time = rospy.Time.now()

    def get_active_command(self):
        now = rospy.Time.now()

        if now - self.last_key_time < self.key_timeout:
            return self.manual_vx, self.manual_vy, self.manual_wz

        if now - self.last_ros_cmd_time < self.ros_cmd_timeout:
            return self.cmd_vx, self.cmd_vy, self.cmd_wz

        return 0.0, 0.0, 0.0

    def publish_odom_and_tf(self, vx_body, vy_body, wz):
        now = rospy.Time.now()
        dt = (now - self.last_odom_time).to_sec()

        if dt <= 0.0:
            dt = self.timestep / 1000.0

        self.last_odom_time = now

        vx_body = -0.02*vx_body
        vy_body = -0.008*vy_body

        dx = (vx_body * math.cos(self.yaw) - vy_body * math.sin(self.yaw)) * dt
        dy = (vx_body * math.sin(self.yaw) + vy_body * math.cos(self.yaw)) * dt
        dyaw = wz * dt

        self.x += dx
        self.y += dy
        self.yaw += dyaw

        q = tf_conversions.transformations.quaternion_from_euler(0, 0, self.yaw)

        t = TransformStamped()
        t.header.stamp = now
        t.header.frame_id = self.odom_frame
        t.child_frame_id = self.base_frame
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        self.tf_br.sendTransform(t)

        odom = Odometry()
        odom.header.stamp = now
        odom.header.frame_id = self.odom_frame
        odom.child_frame_id = self.base_frame

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation.x = q[0]
        odom.pose.pose.orientation.y = q[1]
        odom.pose.pose.orientation.z = q[2]
        odom.pose.pose.orientation.w = q[3]

        odom.twist.twist.linear.x = vx_body
        odom.twist.twist.linear.y = vy_body
        odom.twist.twist.angular.z = wz

        self.odom_pub.publish(odom)

    def publish_scan(self):
        ranges = list(self.lidar.getRangeImage())

        scan = LaserScan()
        scan.header.stamp = rospy.Time.now()
        scan.header.frame_id = self.laser_frame

        n = len(ranges)

        scan.angle_min = -math.pi
        scan.angle_max = math.pi
        scan.angle_increment = (scan.angle_max - scan.angle_min) / max(n - 1, 1)
        scan.range_min = self.lidar.getMinRange()
        scan.range_max = self.lidar.getMaxRange()

   
        scan.ranges = ranges[::-1]

        self.scan_pub.publish(scan)

    def run(self):
        while self.robot.step(self.timestep) != -1 and not rospy.is_shutdown():
            self.poll_keyboard()

            vx_cmd, vy_cmd, wz_cmd = self.get_active_command()

            wheels = self.drive_ik(vx_cmd, vy_cmd, wz_cmd)
            wheels = [self.clamp(w, -self.max_wheel_speed, self.max_wheel_speed) for w in wheels]

            self.m1.setVelocity(wheels[0])
            self.m2.setVelocity(wheels[1])
            self.m3.setVelocity(wheels[2])
            self.m4.setVelocity(wheels[3])

            vx_body, vy_body, wz = self.mecanum_fk(wheels[0], wheels[1], wheels[2], wheels[3])

            self.publish_odom_and_tf(vx_body, vy_body, wz)
            self.publish_scan()

if __name__ == "__main__":
    node = WebotsNavController()
    node.run()