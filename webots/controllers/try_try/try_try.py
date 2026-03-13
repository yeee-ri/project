#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from controller import Robot, Keyboard
import math
import rospy
import tf2_ros

from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan


MOTOR_NAMES = ["OmniR", "OmniFL", "OmniFR"]
BASE_FRAME = "base_link"
ODOM_FRAME = "odom"

WHEEL_R = 0.05
CENTER_TO_WHEEL_L = 0.18

THETAS = [0.0, 2.0 * math.pi / 3.0, 4.0 * math.pi / 3.0]
WHEEL_SIGN = [1.0, 1.0, 1.0]

LIDAR_DEVICE_NAME = "HeadLidar"
LASER_FRAME = "laser"

KEY_LINEAR = 0.4
KEY_ANGULAR = 1.0
KEY_STRAFE = 0.4
KEY_PRIORITY = True


def wrap_pi(a: float) -> float:
    return (a + math.pi) % (2.0 * math.pi) - math.pi


class OmniROSBridge:
    def __init__(self):
        self.robot = Robot()
        self.timestep = int(self.robot.getBasicTimeStep())

        self.motors = []
        for n in MOTOR_NAMES:
            m = self.robot.getDevice(n)
            if m is None:
                raise RuntimeError(f'Device not found: "{n}"')
            m.setPosition(float("inf"))
            m.setVelocity(0.0)
            self.motors.append(m)

        self.gps = self.robot.getDevice("GPS")
        if self.gps is None:
            raise RuntimeError('Device not found: "GPS"')
        self.gps.enable(self.timestep)

        self.imu = self.robot.getDevice("InertialUnit")
        if self.imu is None:
            raise RuntimeError('Device not found: "InertialUnit"')
        self.imu.enable(self.timestep)

        self.lidar = self.robot.getDevice(LIDAR_DEVICE_NAME)
        if self.lidar is None:
            raise RuntimeError(f'Device not found: "{LIDAR_DEVICE_NAME}"')
        self.lidar.enable(self.timestep)
        try:
            self.lidar.enablePointCloud()
        except Exception:
            pass

        self.keyboard = Keyboard()
        self.keyboard.enable(self.timestep)

        self.vx = 0.0
        self.vy = 0.0
        self.wz = 0.0

        self.last_cmd_msg = Twist()
        self.last_cmd_time = rospy.Time(0)
        self.cmd_timeout = rospy.Duration(0.25)

        rospy.Subscriber("/cmd_vel", Twist, self.cb_cmdvel, queue_size=1)
        self.odom_pub = rospy.Publisher("/odom", Odometry, queue_size=10)
        self.scan_pub = rospy.Publisher("/scan", LaserScan, queue_size=10)
        self.tf_br = tf2_ros.TransformBroadcaster()

        self.x0 = None
        self.y0 = None
        self.prev_x = None
        self.prev_y = None
        self.prev_yaw = None
        self.prev_t = None

        self.lidar_fov = None
        self.lidar_hres = None
        self.lidar_min = None
        self.lidar_max = None

    def cb_cmdvel(self, msg: Twist):
        self.last_cmd_msg = msg
        self.last_cmd_time = rospy.Time.now()
        rospy.loginfo("cmd_vel received: vx=%.3f vy=%.3f wz=%.3f",
                  msg.linear.x, msg.linear.y, msg.angular.z)

    def read_keyboard_cmd(self):
        vx = 0.0
        vy = 0.0
        wz = 0.0

        while True:
            k = self.keyboard.getKey()
            if k == -1:
                break

            if k in (ord('W'), ord('w'), Keyboard.UP):
                vx += KEY_LINEAR
            elif k in (ord('S'), ord('s'), Keyboard.DOWN):
                vx -= KEY_LINEAR
            elif k in (ord('A'), ord('a')):
                vy += KEY_STRAFE
            elif k in (ord('D'), ord('d')):
                vy -= KEY_STRAFE
            elif k in (ord('Q'), ord('q'), Keyboard.LEFT):
                wz += KEY_ANGULAR
            elif k in (ord('E'), ord('e'), Keyboard.RIGHT):
                wz -= KEY_ANGULAR
            elif k in (ord('X'), ord('x'), 32):
                vx = 0.0
                vy = 0.0
                wz = 0.0

        return vx, vy, wz

    def get_active_cmd(self):
        now = rospy.Time.now()
        ros_active = (now - self.last_cmd_time) <= self.cmd_timeout

        kx, ky, kz = self.read_keyboard_cmd()
        key_active = (abs(kx) + abs(ky) + abs(kz)) > 0.0

        if KEY_PRIORITY and key_active:
            self.vx, self.vy, self.wz = kx, ky, kz
            return

        if ros_active:
            self.vx = self.last_cmd_msg.linear.x
            self.vy = self.last_cmd_msg.linear.y
            self.wz = self.last_cmd_msg.angular.z
        else:
            self.vx, self.vy, self.wz = (kx, ky, kz) if key_active else (0.0, 0.0, 0.0)

    def set_wheels_from_cmdvel(self):
        ws = []
        for th in THETAS:
            wi = (-math.sin(th) * self.vx + math.cos(th) * self.vy + CENTER_TO_WHEEL_L * self.wz) / WHEEL_R
            ws.append(wi)

        for i, (m, w) in enumerate(zip(self.motors, ws)):
            m.setVelocity(WHEEL_SIGN[i] * w)

    def publish_odom_and_tf(self):
        now = rospy.Time.now()
        t = now.to_sec()

        gx, gy, _gz = self.gps.getValues()
        gx = float(gx)
        gy = float(gy)

        roll, pitch, yaw = self.imu.getRollPitchYaw()
        yaw = float(yaw)

        if self.x0 is None:
            self.x0, self.y0 = gx, gy

        x = gx - self.x0
        y = gy - self.y0

        vx = vy = wz = 0.0
        if self.prev_t is not None:
            dt = max(1e-6, t - self.prev_t)
            vx = (x - self.prev_x) / dt
            vy = (y - self.prev_y) / dt
            dyaw = wrap_pi(yaw - self.prev_yaw)
            wz = dyaw / dt

        self.prev_x, self.prev_y, self.prev_yaw, self.prev_t = x, y, yaw, t

        qz = math.sin(yaw * 0.5)
        qw = math.cos(yaw * 0.5)

        ts = TransformStamped()
        ts.header.stamp = now
        ts.header.frame_id = ODOM_FRAME
        ts.child_frame_id = BASE_FRAME
        ts.transform.translation.x = x
        ts.transform.translation.y = y
        ts.transform.translation.z = 0.0
        ts.transform.rotation.x = 0.0
        ts.transform.rotation.y = 0.0
        ts.transform.rotation.z = qz
        ts.transform.rotation.w = qw
        self.tf_br.sendTransform(ts)

        od = Odometry()
        od.header.stamp = now
        od.header.frame_id = ODOM_FRAME
        od.child_frame_id = BASE_FRAME
        od.pose.pose.position.x = x
        od.pose.pose.position.y = y
        od.pose.pose.position.z = 0.0
        od.pose.pose.orientation.z = qz
        od.pose.pose.orientation.w = qw
        od.twist.twist.linear.x = vx
        od.twist.twist.linear.y = vy
        od.twist.twist.angular.z = wz
        self.odom_pub.publish(od)

    def publish_scan(self):
        if self.lidar_fov is None:
            self.lidar_fov = float(self.lidar.getFov())
            self.lidar_hres = int(self.lidar.getHorizontalResolution())
            self.lidar_min = float(self.lidar.getMinRange())
            self.lidar_max = float(self.lidar.getMaxRange())

        ranges = self.lidar.getRangeImage()
        if ranges is None:
            return

        now = rospy.Time.now()
        scan = LaserScan()
        scan.header.stamp = now
        scan.header.frame_id = LASER_FRAME

        fov = self.lidar_fov
        hres = self.lidar_hres
        scan.angle_min = -0.5 * fov
        scan.angle_max = 0.5 * fov
        scan.angle_increment = fov / max(1, (hres - 1))
        scan.time_increment = 0.0
        scan.scan_time = self.timestep / 1000.0
        scan.range_min = self.lidar_min
        scan.range_max = self.lidar_max

        cleaned = []
        rmin = scan.range_min
        rmax = scan.range_max
        for r in ranges:
            rr = float(r)
            if math.isnan(rr) or math.isinf(rr):
                cleaned.append(rmax)
            else:
                if rr < rmin:
                    cleaned.append(rmin)
                elif rr > rmax:
                    cleaned.append(rmax)
                else:
                    cleaned.append(rr)

        scan.ranges = cleaned
        self.scan_pub.publish(scan)

    def run(self):
        rate_hz = 1000.0 / float(self.timestep)
        r = rospy.Rate(rate_hz)

        while self.robot.step(self.timestep) != -1 and not rospy.is_shutdown():
            self.get_active_cmd()
            self.set_wheels_from_cmdvel()
            self.publish_odom_and_tf()
            self.publish_scan()
            r.sleep()


if __name__ == "__main__":
    rospy.init_node("webots_omni_bridge", anonymous=True)
    OmniROSBridge().run()
