# Step 1: Base Image
FROM ros:foxy

SHELL ["/bin/bash", "-c"]

# Step 2: Dependencies
# Update and install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    sudo \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install \
    pyserial  # Install pyserial
    
# ROS2 dependencies
RUN apt-get update && apt-get install -y \
    ros-foxy-xacro \
    ros-foxy-rmw-cyclonedds-cpp \
    ros-foxy-robot-state-publisher \
    ros-foxy-joint-state-publisher \
    ros-foxy-robot-localization \
    ros-foxy-rtabmap-ros \
    ros-foxy-nav2-bringup \
    ros-foxy-slam-toolbox \
    ros-foxy-realsense2-camera \
    # Add more ROS2 package dependencies as needed
    && rm -rf /var/lib/apt/lists/*

# Step 3: Copy Your Package and ros_entrypoint.sh
WORKDIR /ros2_ws/src

# Clone the sllidar_ros2 package
RUN git clone https://github.com/Slamtec/sllidar_ros2.git

# Copy your custom package
COPY ./push_mapping ./push_mapping

# Step 4: Build Your Package and sllidar_ros2
WORKDIR /ros2_ws
RUN . /opt/ros/foxy/setup.sh && \
    colcon build --symlink-install
COPY ros-entrypoint.sh /

# Make ros_entrypoint.sh executable
RUN chmod +x /ros-entrypoint.sh



# Step 5: Set the entrypoint script
ENTRYPOINT ["/ros-entrypoint.sh"]
CMD ["/bin/bash"]

