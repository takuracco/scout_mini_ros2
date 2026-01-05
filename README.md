scout_mini_ros2

# 環境
ubuntu 22.04
ROS2 Humble

# topic
|トピック名|データ型|pub/sub|詳細|
|--|--|--|--|
|/diff_drive_controller/cmd_vel_unstamped|Twist|sub|scout_miniに与える速度情報|
|/scan|PointCloud2|pub|LiDARの点群データ。XT32想定|
|/robot_description|???|pub|ロボットの機体データ|

# コマンド
起動コマンド
`ros2 launch scout_mini_gazebo_sim sim.launch.py`

# 必要パッケージ
 `ros-humble-ros-base`
 `ros-humble-xacro`
 `ros-humble-robot-state-publisher`
 `ros-humble-joint-state-publisher`
 `ros-humble-gazebo-ros`
 `ros-humble-gazebo-ros-pkgs`
 `gazebo`
 `ros-humble-ros2-control`
 `ros-humble-ros2-controllers`
 `ros-humble-gazebo-ros2-control`
 `ros-humble-diff-drive-controller`
 `ros-humble-rviz2`
 `topic_tools`