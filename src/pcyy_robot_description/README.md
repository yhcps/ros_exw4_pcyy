# pcyy_robot_description (ROS1)

本包包含一个简单的机器人描述模型：

- `base_link`（底盘）
- `wheel_left_link`（左轮）
- `wheel_right_link`（右轮）
- `caster_link`（万向轮）
- `lidar_link`（简化激光雷达，固定在底盘）

关节配置：

- `wheel_left_joint` / `wheel_right_joint`: `revolute`，绕 `Y` 轴
- `caster_joint`: `fixed`

## 目录

- `urdf/simple_robot.urdf`（原始 URDF 参考）
- `urdf/simple_robot.xacro`（主文件，模块化入口）
- `urdf/common_properties.xacro`（参数与惯量宏）
- `urdf/chassis.xacro`（底盘+万向轮）
- `urdf/wheels.xacro`（轮子宏与关节）
- `urdf/sensors.xacro`（激光雷达宏）
- `urdf/gazebo_plugins.xacro`（Gazebo插件与接触参数）
- `launch/display.launch`
- `launch/check_urdf.launch`
- `launch/gazebo.launch`
- `rviz/simple_robot.rviz`

## 运行（ROS1）

1. 编译工作空间后 source 环境
2. 在 RViz 查看模型（从 xacro 加载）：

```bash
roslaunch pcyy_robot_description display.launch
```

3. 快速检查 xacro/URDF 结构：

```bash
roslaunch pcyy_robot_description check_urdf.launch
```

4. 启动 Gazebo 仿真（从 xacro 加载并 spawn）：

```bash
roslaunch pcyy_robot_description gazebo.launch
```

5. 验证话题（应看到 `/cmd_vel`、`/odom`）：

```bash
rostopic list
```

6. 键盘控制小车：

```bash
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```

## 说明

- 已配置 `libgazebo_ros_diff_drive.so` 插件，`leftJoint/rightJoint` 与 URDF 中关节名一致：
	- `wheel_left_joint`
	- `wheel_right_joint`
- 插件订阅 `/cmd_vel` 并发布 `/odom`，可直接用于 Gazebo 中运动控制。
