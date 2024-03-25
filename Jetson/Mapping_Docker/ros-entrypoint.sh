#!/bin/bash
set -e

# source ROS 2 setup files
source "/opt/ros/foxy/setup.bash"
source "/ros2_ws/install/setup.bash"

ros2 launch push_mapping push_mapping.launch.py
# execute the passed command
exec "$@"
