#!/usr/bin/python3
# -*- coding: utf-8 -*-

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, TextSubstitution, PythonExpression
from launch_ros.actions import Node
import os
from ament_index_python import get_package_share_directory

def generate_launch_description():

    # Package name
    package_name = 'vikings_bot_map_server'

    # Parmaters
    map_file_name_arg = DeclareLaunchArgument('map_file',
                                            default_value='simulation_map.yaml',
                                            description='Choose real vs simulated map')
    use_rviz_arg = DeclareLaunchArgument('use_rviz',
                                            default_value='False',
                                            description='Choose use or not use RVIZ')

    map_file_name_val = LaunchConfiguration('map_file')
    use_rviz_val = LaunchConfiguration('use_rviz')


    # RVIZ node
    rviz_config = os.path.join(get_package_share_directory(package_name), 'rviz', 'map_server.rviz')
    rviz_node = Node(package='rviz2',
                    executable='rviz2',
                    name='rviz2',
                    output='screen',
                    condition=IfCondition(PythonExpression([use_rviz_val])),
                    arguments=['-d', rviz_config]
                    )
    
    # Map server
    map_file_path = PathJoinSubstitution([get_package_share_directory(package_name), 'maps', map_file_name_val])

    map_server_node = Node(package='nav2_map_server',
                            executable='map_server',
                            name='map_server',
                            output='screen',
                            parameters=[{'use_sim_time': True},
                                        {"topic_name": "map"},
                                        {"frame_id": "map"},
                                        {'yaml_filename': map_file_path}])


    # Lifecycle node
    lifecycle_node = Node(package='nav2_lifecycle_manager',
                            executable='lifecycle_manager',
                            name='map_server_lifecycle_manager',
                            output='screen',
                            parameters=[{'use_sim_time': True},
                                        {'autostart': True},
                                        {'node_names': ['map_server']}])
                    


    return LaunchDescription([  map_file_name_arg,
                                use_rviz_arg,
                                LogInfo(msg=map_file_path),
                                rviz_node,
                                map_server_node,
                                lifecycle_node
    ])