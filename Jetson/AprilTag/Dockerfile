# Use the official ROS Foxy base image
FROM ros:foxy

# Use bash shell for RUN commands
SHELL ["/bin/bash", "-c"]

# Update and install necessary packages
RUN apt-get update && apt-get install -y \
    # Install Cyclone DDS if not included in the base image
    ros-foxy-rmw-cyclonedds-cpp \
    # Install development tools
    build-essential \
    cmake \
    git \
    python3-pip \
    python3-rosdep \
    libboost-python-dev
 
    # Clean apt cache to reduce image size


# Install Python dependencies
RUN pip3 install --force-reinstall numpy 
RUN pip3 install numpy pupil-apriltags transforms3d

# Create and initialize ROS2 workspace
ENV ROS_WS=/opt/ros_ws

RUN mkdir -p ${ROS_WS}/src

# Clone necessary repositories--yes install ros-foxy-vision-opencv


# Copy your ROS2 package if necessary
WORKDIR ${ROS_WS}
RUN . /opt/ros/foxy/setup.sh && sudo apt --yes install python3-opencv && sudo apt install --yes ros-foxy-image-transport && rosdep update 

RUN cd src && git clone -b 3.0.2 https://github.com/ros-perception/vision_opencv.git
COPY ./apriltag_ros2 ${ROS_WS}/src/apriltag_ros2


    
WORKDIR ${ROS_WS}   
RUN . /opt/ros/foxy/setup.sh && rosdep install -i --from-path src --rosdistro foxy -y -r   

#RUN apt-get update && apt-get install -y \
 #   ros-foxy-cv-bridge 

# Build the workspace
RUN . /opt/ros/foxy/setup.sh && colcon build


# Configure the environment
RUN echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc \
    && echo "source ${ROS_WS}/install/setup.bash" >> ~/.bashrc \
    && echo "export ROS_DOMAIN_ID=2" >> ~/.bashrc \
    && echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Copy configuration and launch files if necessary
COPY tags_36h11_filter.yaml ${ROS_WS}/src/apriltag_ros/apriltag_ros/cfg/
#COPY tag_realsense.launch.py ${ROS_WS}/src/apriltag_ros/apriltag_ros/launch/
#RUN chmod +x ${ROS_WS}/src/apriltag_ros/apriltag_ros/launch/tag_realsense.launch.py

# Custom entrypoint script
COPY ./ros_entrypoint.sh /
RUN chmod +x /ros_entrypoint.sh 

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
# CMD ["ros2", "launch", "apriltag_ros", "tag_realsense.launch.py"]

