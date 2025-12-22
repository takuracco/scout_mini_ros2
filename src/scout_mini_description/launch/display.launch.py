from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg = get_package_share_directory('scout_mini_description')
    default_model = os.path.join(pkg, 'urdf', 'scout_mini.urdf.xacro')
    default_rviz  = os.path.join(pkg, 'rviz', 'scout_mini.rviz')

    control_yaml = PathJoinSubstitution([
        FindPackageShare("scout_mini_control"),
        "config",
        "scout_mini_control.yaml",
    ])

    model = LaunchConfiguration('model')
    rviz_config = LaunchConfiguration('rvizconfig')
    use_sim_time = LaunchConfiguration('use_sim_time')

    return LaunchDescription([
        DeclareLaunchArgument('model', default_value=default_model),
        DeclareLaunchArgument('rvizconfig', default_value=default_rviz),
        DeclareLaunchArgument('use_sim_time', default_value='false'),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': Command(['xacro ', model, ' ros2_control_yaml:=', control_yaml]),
                'use_sim_time': use_sim_time,
            }],
            output='screen',
        ),

        # JointStatePublisher（固定関節しかないなら不要だけど、入れておくと便利）
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            output='screen',
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen',
        ),
    ])