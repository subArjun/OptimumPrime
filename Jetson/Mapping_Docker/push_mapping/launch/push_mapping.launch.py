# pylint: skip-file
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess,IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution
from launch_ros.actions import Node
import os
import xacro


#path to rviz config
rviz_dir = os.path.join(get_package_share_directory('push_mapping'), 'rviz', 'push_mapping.rviz')
urdf_file_path = os.path.join(get_package_share_directory('push_mapping'), 'description', 'push_mapping.xacro') #optimum_primte for full robot

def generate_launch_description():
	#process the xacro macros 
    robot_description = xacro.process_file(urdf_file_path).toxml()
	#launch description
    #Robot state publisher node which publishes the tf tree for the robot based on the provided description file
    usb_command = ExecuteProcess(
    	cmd=[['echo team13 | sudo -S chmod 0777 /dev/ttyUSB*']],
    	shell=True,
    )

    arduino_command = ExecuteProcess(
    	cmd=[['echo team13 | sudo -S chmod 0777 /dev/arduino']],
    	shell=True,
    )


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
    
    #Node to launch the lidar and publish data over the scan topic
    lidar = Node(
        package='sllidar_ros2',
        executable='sllidar_node',
        name='sllidar_node',
        parameters=[{'channel_type': 'serial',
                        'serial_port': '/dev/lidar', 
                        'serial_baudrate': 256000, 
                        'frame_id': 'base_scan',
                        'inverted': False, 
                        'angle_compensate': True,
                        'use_sim_time': False}],
        output='screen',
        
    )
    
    #launch file to launch the Intel RealSense D415 camera and publish color and rectified depth data over the ros network
    realsense = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py'])
            ]),
        launch_arguments={'enable_rgbd': 'true', 'enable_sync': 'true', 'align_depth.enable': 'true', 'enable_color': 'true', 'enable_depth': 'true', 'use_sim_time':'false'}.items()
    )
    
    #node to generate one source of odometry from the lidar data using iterative Closest Point
    icpOdom = Node(
        package='rtabmap_odom',
        executable='icp_odometry',
        parameters=[{'frame_id': 'base_link', 'publish_tf': False, 'use_sim_time': False}],
        remappings=[('/odom', '/odom0')],
        output='log'
    )
    
    #Node to generate another source of odometry from RGBD camera data using feature matching
    rgbdOdom = Node(
        package='rtabmap_odom',
        executable='rgbd_odometry',
        parameters=[{'frame_id': 'base_link', 'publish_tf': False, 'approx_sync': False, 'use_sim_time': False}],
        remappings=[('/odom', '/odom1'), ('/rgb/image', '/camera/color/image_raw'), ('/depth/image', '/camera/depth/image_rect_raw'), ('/rgb/camera_info', '/camera/color/camera_info')],
        output='log'
    )
    
    #Node to fuse the two odometry sources to provide a single filtered odometry source using enxtended Kalmann filtering
    localization = Node(
        package='robot_localization',
        executable='ekf_node',
        parameters=[{
            'frequency': 40.0, 
            'two_d_mode': True, 
            'sensor_timeout':0.1,
            'map_frame': "map", 
            'odom_frame': "odom",
            'use_sim_time': False, 
            'base_link_frame': "base_link",
            'publish_tf': True,
            'predict_to_current_time': True, 
            'world_frame': "odom", 
            'odom0': "odom0", 
            'odom0_config': [
                True,  True,  False,
                False, False, True,
                False, False, False,
                False, False, False,
                False, False, False
            ], 
            'odom1': "odom1", 
            'odom1_config': [
                True,  True,  False,
                False, False, True,
                False, False, False,
                False, False, False,
                False, False, False
            ]
        }],
        #arguments=['--ros-args', '--log-level', 'debug'],
        remappings=[('/odometry/filtered', '/odom')]
    )
    
    #launch file to bringup up a navigation stack
    navCore = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([get_package_share_directory('nav2_bringup'), 'launch', 'navigation_launch.py'])
        ]),
        launch_arguments={'use_sim_time' : 'false', 'use_respawn' : 'true'}.items(),
    )
    
    #launch file to launch the slam_toolbox asynchronous mapping
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py'])
        ]),
        launch_arguments={'use_sim_time' : 'false'}.items(),
    )
    
    
    
    #launch file to bringup up a nav2 configuration of RVIZ
    rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([get_package_share_directory('nav2_bringup'), 'launch', 'rviz_launch.py'])
        ]),
        launch_arguments={'rviz_config': rviz_dir}.items()
    )

    rtabmap = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([get_package_share_directory('rtabmap_launch'), 'launch', 'rtabmap.launch'])
        ]),
        launch_arguments = {'frame_id':'base_link', 'approx_sync':'false', 'rgb_topic':'/camera/color/image_raw', 'depth_topic':'/camera/aligned_depth_to_color/image_raw', 'subscribe_scan': 'true', 'visual_odometry':'false', 'camera_info_topic':'/camera/color/camera_info', 'scan_cloud_assembling':'true', 'use_sim_time':'false'}.items()
    )
    
    bringup = Node(
        package='push_mapping',
        executable='bringup'
    )
    
        
        
    return LaunchDescription([
        usb_command,
        arduino_command,
    	description,
        jointState,
        lidar,
        realsense,
        TimerAction(
        	period=3.0,
        	actions=[icpOdom,rgbdOdom]
        ),
        TimerAction(
        	period=6.0,
        	actions=[localization]
        ),
        TimerAction(
        	period=8.0,
        	actions=[navCore]
        ),
        TimerAction(
        	period=14.0,
        	actions=[slam]
        ),
        TimerAction(
        	period=16.0,
        	actions=[bringup]
        )
    ])

