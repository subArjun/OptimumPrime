# Step 1: Base Image
FROM osrf/ros:foxy-desktop

SHELL ["/bin/bash", "-c"]

# Step 2: Dependencies
# Update and install system dependencies
RUN apt-get update && apt-get install -y \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# ROS2 dependencies
RUN apt-get update && apt-get install -y \
    ros-foxy-xacro \
    ros-foxy-rmw-cyclonedds-cpp \
    ros-foxy-robot-state-publisher \
    ros-foxy-joint-state-publisher \
    ros-foxy-rtabmap-ros \
    ros-foxy-nav2-bringup \
    ros-foxy-slam-toolbox \
    # Add more ROS2 package dependencies as needed
    && rm -rf /var/lib/apt/lists/*

# Step 3: Copy Your Package and ros_entrypoint.sh
COPY ./push_mapping /ros2_ws/src/push_mapping
COPY ros_entrypoint.sh /

# Make ros_entrypoint.sh executable
RUN chmod +x /ros_entrypoint.sh

# Step 4: Build Your Package
WORKDIR /ros2_ws
RUN . /opt/ros/foxy/setup.sh && \
    colcon build --symlink-install

# Step 5: Set the entrypoint script
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["/bin/bash"]

