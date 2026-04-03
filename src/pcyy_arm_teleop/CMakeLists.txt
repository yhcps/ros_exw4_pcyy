cmake_minimum_required(VERSION 3.0.2)
project(pcyy_arm_teleop)

find_package(catkin REQUIRED COMPONENTS
  rospy
  sensor_msgs
  trajectory_msgs
)

catkin_package()

catkin_install_python(PROGRAMS
  scripts/arm_keyboard_teleop.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch config
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
