SIMULATION:
webots home_service.wbt 

rosrun tf2_ros static_transform_publisher 0 0 0 0 0 0 base_link laser

roslaunch hector_slam_launch tutorial.launch base_frame:=base_link odom_frame:=odom scan_topic:=/scan
