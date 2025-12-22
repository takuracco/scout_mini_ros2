cmake_minimum_required(VERSION 3.8)
project(scout_mini_gazebo_sim)

find_package(ament_cmake REQUIRED)

# Install launch/worlds/models so they appear in install/share/<pkg>/
install(DIRECTORY
  launch
  worlds
  models
  DESTINATION share/${PROJECT_NAME}
)

ament_package()