# pcyy_robot_description

本仓库是教具机器人仿真与机械臂键盘控制工作空间（ROS Noetic / Gazebo）。

## 目录说明

- `src/pcyy_robot_description/`：机器人描述与基础仿真启动文件
- `src/pcyy_arm_teleop/`：机械臂键盘控制功能包（参数化按键映射）
- `run_arm_only.sh`：一键启动脚本（支持 GUI / 无 GUI）

## 快速开始

在工作空间根目录运行：

```bash
cd ~/workspace/pcyy_robot_description
./run_arm_only.sh
```

如果 Gazebo 黑窗，使用无 GUI 模式：

```bash
cd ~/workspace/pcyy_robot_description
GAZEBO_GUI=0 ./run_arm_only.sh
```

## 机械臂键盘控制

默认控制 5 个关节：`joint_1 ~ joint_5`。

按键映射在：

- `src/pcyy_arm_teleop/config/arm_teleop.yaml`

核心思路：按键映射到关节目标增量，并发布到：

- `/arm_joint_controller/command` (`trajectory_msgs/JointTrajectory`)

## 常见问题

1. 控制器加载失败：

- 现象：`position_controllers/JointTrajectoryController does not exist`
- 处理：安装 `ros-noetic-joint-trajectory-controller` 与 `ros-noetic-ros-controllers`

2. Gazebo 黑窗：

- 优先用 `GAZEBO_GUI=0 ./run_arm_only.sh`

3. 按键没反应：

- 确认 `arm_joint_controller` 已成功 `load/start`
- 确认终端在运行键盘节点窗口中（非后台无TTY）

## 相关文档

- `src/pcyy_arm_teleop/README.md`
- `src/pcyy_robot_description/README.md`
