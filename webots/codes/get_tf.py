#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import tf
import sys
import select
import tty
import termios
import os

def main():
    rospy.init_node('tf_position_reader')
    listener = tf.TransformListener()
    rate = rospy.Rate(2) 

    file_path = "/home/sj/Desktop/project/webots/codes/data.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)

    try:
        while not rospy.is_shutdown():
            try:
                (trans, rot) = listener.lookupTransform('/map', '/base_link', rospy.Time(0))
                x, y, z = trans
                r,p,yaw,w = rot

               
                print(f"{x:.3f} {y:.3f} {z:.3f} {r:.3f} {p:.3f} {yaw:.3f} {w:.3f}")

                
                if select.select([sys.stdin], [], [], 0)[0]:
                    char = sys.stdin.read(1)

                    if char == 'z':
                        with open(file_path, "a") as f:
                            f.write(f"{x:.3f} {y:.3f} {z:.3f} {r:.3f} {p:.3f} {yaw:.3f} {w:.3f}\n")
                        print("saved")

                rate.sleep()

            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                rate.sleep()

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if __name__ == '__main__':
    main()