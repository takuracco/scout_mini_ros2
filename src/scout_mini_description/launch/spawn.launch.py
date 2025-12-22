from launch import LaunchDescription
from launch.actions import TimerAction
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    xacro_file = PathJoinSubstitution([
        FindPackageShare('scout_mini_description'),
        'urdf',
        'scout_mini.urdf.xacro'
    ])

    robot_description = Command(['xacro ', xacro_file])

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description,
                     'use_sim_time': True}],
        output='screen'
    )

    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'scout_mini',
            '-topic', '/robot_description',
            '-x', '0', '-y', '0', '-z', '0.2',
        ],
        output='screen'
    )

    return LaunchDescription([
        rsp,
        TimerAction(period=2.0, actions=[spawn]),
    ])