#!/bin/bash
set -e

# source ROS 2 setup files
source "/opt/ros/foxy/setup.bash"
source "/ros2_ws/install/setup.bash"
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export ROS_DOMAIN_ID=2

ros2 launch push_mapping push_mapping.launch.py
# execute the passed command
exec "$@"
