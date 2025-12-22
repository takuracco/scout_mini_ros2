scout_mini_ros2

# 環境
ubuntu 22.04
ROS2 Humble

# topic
|トピック名|データ型|pub/sub|詳細|
|--|--|--|--|
|cmd_vel|Twist|sub|scout_miniに与える速度情報|
|scan|PointCloud2|pub|LiDARの点群データ。XT32想定|
|robot_description|???|pub|ロボットの機体データ|

# コマンド
rviz表示
'ros2 launch scout_mini_description display.launch.py'

gazeboスポーン
'ros2 launch scout_mini_description spawn.launch.py'

すべて起動
'ros2 launch scout_mini_gazebo_sim sim.launch.py'