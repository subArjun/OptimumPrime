#!/bin/bash
set -e

source /opt/ros/foxy/setup.bash
source /opt/ros_ws/install/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export ROS_DOMAIN_ID=2
ros2 run apriltag_ros2 april

exec "$@"
