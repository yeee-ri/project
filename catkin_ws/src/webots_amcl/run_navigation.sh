#!/bin/bash

xhost +local:docker > /dev/null 2>&1

tmux kill-session -t main 2>/dev/null
tmux new-session -d -s main

tmux set-environment -t main DISPLAY $DISPLAY
tmux set-environment -t main XAUTHORITY $XAUTHORITY

tmux set -g mouse on
tmux split-window -h
tmux select-pane -t 0
tmux split-window -v
tmux select-pane -t 2
tmux split-window -v

COMMON_ENV="source /opt/ros/noetic/setup.bash && source ~/Desktop/project/catkin_ws/devel/setup.bash"

# 1. roscore
tmux select-pane -t 0
tmux send "$COMMON_ENV && roscore" C-m
sleep 2

# 2. Webots
tmux select-pane -t 1
tmux send "$COMMON_ENV && cd ~/Desktop/project/webots/worlds/ && webots home_service.wbt" C-m
sleep 2

# 3. move_base 
tmux select-pane -t 2
tmux send "$COMMON_ENV && roslaunch webots_amcl move_base_amcl.launch" C-m
sleep 3

# 4. amcl_diff
tmux select-pane -t 3
tmux send "$COMMON_ENV && roslaunch webots_amcl amcl_diff.launch" C-m

tmux select-layout tiled
tmux attach-session -t main