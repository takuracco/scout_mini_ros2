cmake_minimum_required(VERSION 3.8)
project(scout_mini_control)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()