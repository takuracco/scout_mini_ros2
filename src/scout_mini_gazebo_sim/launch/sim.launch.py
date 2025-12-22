from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, EnvironmentVariable, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    sim_share = FindPackageShare('scout_mini_gazebo_sim')
    desc_share = FindPackageShare('scout_mini_description')

    # worldモデル(testworld) と robotモデル(scout_mini_description) の両方を通す
    set_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=[
            PathJoinSubstitution([sim_share, 'models']),
            ':',
            PathJoinSubstitution([desc_share, '..']),
            ':',
            '/usr/share/gazebo-11/models',
        ]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('gazebo_ros'), 'launch', 'gazebo.launch.py'])
        ),
        launch_arguments={
            'world': PathJoinSubstitution([sim_share, 'worlds', 'testworld.world']),
        }.items()
    )

    control_yaml = PathJoinSubstitution([
        FindPackageShare("scout_mini_control"),
        "config",
        "scout_mini_control.yaml",
    ])

    robot_description = {
        "robot_description": Command([
            "xacro ",
            PathJoinSubstitution([
                FindPackageShare("scout_mini_description"),
                "urdf",
                "scout_mini.urdf.xacro",
            ]),
            " ros2_control_yaml:=",
            control_yaml,
        ])
    }


    # control_node = Node(
    #     package="controller_manager",
    #     executable="ros2_control_node",
    #     parameters=[
    #         robot_description,
    #         PathJoinSubstitution([
    #             FindPackageShare("scout_mini_control"),
    #             "config",
    #             "scout_mini_control.yaml",
    #         ]),
    #     ],
    #     output="screen"
    # )

    rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([desc_share, 'launch', 'display.launch.py'])
        )
    )

    spawn_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([desc_share, 'launch', 'spawn.launch.py'])
        )
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller", "--controller-manager", "/controller_manager"],
    )

    return LaunchDescription([
        set_model_path,
        gazebo,
        spawn_robot,
        # control_node,
        joint_state_broadcaster_spawner,
        diff_drive_spawner,
        rviz,
    ])
