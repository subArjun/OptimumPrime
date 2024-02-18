from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution
from launch_ros.actions import Node
import os
import xacro


def generate_launch_description():
	
    rtabmap = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([get_package_share_directory('rtabmap_launch'), 'launch', 'rtabmap.launch.py'])
        ]),
        launch_arguments = {'frame_id':'base_link', 'approx_sync':'false', 'rgb_topic':'/camera/color/image_raw', 'depth_topic':'/camera/aligned_depth_to_color/image_raw', 'subscribe_scan': 'false', 'visual_odometry':'true', 'camera_info_topic':'/camera/color/camera_info', 'scan_cloud_assembling':'true', 'queue_size':'10', 'use_sime_time':'false', 'rtabviz':'false','rviz':'true'}.items(),
    )
    urdf_file_path = os.path.join(get_package_share_directory('push_mapping'), 'description', 'push_mapping.xacro') #optimum_primte for full robot
    robot_description = xacro.process_file(urdf_file_path).toxml()
	#launch description
    #Robot state publisher node which publishes the tf tree for the robot based on the provided description file
    description = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': False}],
    )
    
    #The joint state publisher publishes dummy joint state values for our wheel joints. This is required for the publishing of continuous joints in robot_state_publisher
    jointState = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': False}],
    )
    realsense = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py'])
            ]),
        launch_arguments={'enable_rgbd': 'true', 'enable_sync': 'true', 'align_depth.enable': 'true', 'enable_color': 'true', 'enable_depth': 'true', 'use_sim_time':'false'}.items()
    )
    rgbdOdom = Node(
        package='rtabmap_odom',
        executable='rgbd_odometry',
        parameters=[{'frame_id': 'base_link', 'publish_tf': False, 'approx_sync': False, 'use_sim_time': False}],
        remappings=[('/rgb/image', '/camera/color/image_raw'), ('/depth/image', '/camera/depth/image_rect_raw'), ('/rgb/camera_info', '/camera/color/camera_info')],
        output='log'
    )
   
    return LaunchDescription([description,jointState,realsense,rtabmap])
