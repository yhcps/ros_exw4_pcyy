#!/usr/bin/env bash
set -e

cd /home/bcsh/workspace/pcyy_robot_description

source /opt/ros/noetic/setup.bash
source /home/bcsh/upros_sim/devel/setup.bash

if [ -f /home/bcsh/workspace/pcyy_robot_description/devel/setup.bash ]; then
  source /home/bcsh/workspace/pcyy_robot_description/devel/setup.bash
fi

# 黑窗兼容：默认使用软件渲染（可覆盖）
export LIBGL_ALWAYS_SOFTWARE="${LIBGL_ALWAYS_SOFTWARE:-1}"
export MESA_GL_VERSION_OVERRIDE="${MESA_GL_VERSION_OVERRIDE:-3.3}"
export SVGA_VGPU10="${SVGA_VGPU10:-0}"

# 可通过环境变量切换是否打开 Gazebo GUI
# GAZEBO_GUI=0 ./run_arm_only.sh  -> 无界面（仅仿真+控制）
if [ "${GAZEBO_GUI:-1}" = "0" ]; then
  roslaunch pcyy_arm_teleop arm_keyboard_teleop.launch gui:=false headless:=true
else
  roslaunch pcyy_arm_teleop arm_keyboard_teleop.launch gui:=true headless:=false
fi
