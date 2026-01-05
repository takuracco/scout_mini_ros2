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

    control_yaml = PathJoinSubstitution([
        FindPackageShare("scout_mini_control"),
        "config",
        "scout_mini_control.yaml",
    ])

    robot_description = Command([
        'xacro ', xacro_file,
        ' ros2_control_yaml:=', control_yaml
    ])

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

    cmd_vel_relay = Node(
        package="topic_tools",
        executable="relay",
        arguments=[
            "/cmd_vel",
            "/diff_drive_controller/cmd_vel_unstamped",
        ],
        output="screen",
    )

    return LaunchDescription([
        rsp,
        TimerAction(period=2.0, actions=[spawn]),
        cmd_vel_relay,
    ])
