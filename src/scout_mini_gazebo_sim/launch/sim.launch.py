from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, TimerAction, ExecuteProcess
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')

    sim_share  = FindPackageShare('scout_mini_gazebo_sim')
    desc_share = FindPackageShare('scout_mini_description')

    world_file = PathJoinSubstitution([sim_share, 'worlds', 'testworld.world'])

    control_yaml = PathJoinSubstitution([
        FindPackageShare('scout_mini_control'),
        'config',
        'scout_mini_control.yaml',
    ])

    xacro_file = PathJoinSubstitution([desc_share, 'urdf', 'scout_mini.urdf.xacro'])
    robot_description = Command([
        'xacro ', xacro_file,
        ' ros2_control_yaml:=', control_yaml
    ])

    set_gazebo_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=[
            PathJoinSubstitution([sim_share, 'models']),
            ':',
            PathJoinSubstitution([desc_share, '..']),
            ':',
            '/usr/share/gazebo-11/models',
        ]
    )

    # ★ここがポイント：gzserver/gzclientはExecuteProcessで起動する
    gzserver = ExecuteProcess(
        cmd=[
            'gzserver',
            world_file,
            '-s', 'libgazebo_ros_init.so',
            '-s', 'libgazebo_ros_factory.so',
            '-s', 'libgazebo_ros_force_system.so',
        ],
        output='screen',
    )

    # GUIが落ちるなら一旦コメントアウトでOK
    gzclient = ExecuteProcess(
        cmd=['gzclient'],
        output='screen',
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': use_sim_time,
        }],
        output='screen',
    )

    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'scout_mini', '-topic', '/robot_description', '-x', '0.5', '-y', '0.5', '-z', '0.2'],
        output='screen',
    )

    jsb_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        output='screen',
    )
    diff_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['diff_drive_controller', '--controller-manager', '/controller_manager'],
        output='screen',
    )

    rviz_config = PathJoinSubstitution([desc_share, 'rviz', 'scout_mini.rviz'])
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen',
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        set_gazebo_model_path,

        gzserver,
        gzclient,  # GUI不要なら消す/コメントアウト

        rsp,
        TimerAction(period=2.0, actions=[spawn]),
        TimerAction(period=6.0, actions=[jsb_spawner, diff_spawner]),
        rviz,
    ])
