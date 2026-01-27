from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

def generate_launch_description():
    config_dir = FindPackageShare("scout_mini_gazebo_sim")
    configuration_directory = PathJoinSubstitution([config_dir, "config"])
    configuration_basename = "scout_3d.lua"  # ここは実ファイル名に合わせる

    carto = Node(
        package="cartographer_ros",
        executable="cartographer_node",
        arguments=[
            "-configuration_directory", configuration_directory,
            "-configuration_basename", configuration_basename,
        ],
        remappings=[
            ('points2', '/scan'),
            ('odom', '/ground_truth/odom'),
        ],
        parameters=[{"use_sim_time": True}],
        output="screen",
    )

    return LaunchDescription([carto])
