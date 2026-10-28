from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # Launch引数
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    yaw = LaunchConfiguration('yaw')

    # Xacroファイル
    xacro_file = PathJoinSubstitution([
        FindPackageShare('scout_mini_description'),
        'urdf',
        'scout_mini.urdf.xacro'
    ])

    # Robot Description
    robot_description = Command([
        'xacro ',
        xacro_file
    ])

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }],
        output='screen'
    )

    # Spawn
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'scout_mini',
            '-topic', '/robot_description',
            '-x', x,
            '-y', y,
            '-z', z,
            '-Y', yaw
        ],
        output='screen'
    )

    # Controller
    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            '/controller_manager'
        ],
        output='screen'
    )

    diff_drive_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'diff_drive_controller',
            '--controller-manager',
            '/controller_manager'
        ],
        output='screen'
    )

    return LaunchDescription([

    DeclareLaunchArgument('x', default_value='0.0'),
    DeclareLaunchArgument('y', default_value='0.5'),
    DeclareLaunchArgument('z', default_value='0.0'),
    DeclareLaunchArgument('yaw', default_value='0.0'),

    robot_state_publisher,

    TimerAction(
        period=2.0,
        actions=[spawn_entity]
    ),

    TimerAction(
        period=6.0,
        actions=[
            joint_state_broadcaster,
            diff_drive_controller
        ]
    )
])