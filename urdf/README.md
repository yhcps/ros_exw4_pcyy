# Two Wheel Cart URDF

该目录包含一个两轮长方体小车模型：`two_wheel_cart.urdf`。

## 模型说明

- 车体：长方体 `0.50 x 0.35 x 0.12 m`
- 轮子：半径 `0.08 m`，厚度 `0.05 m`
- 轮距：`0.30 m`（左右轮中心间距）
- 坐标系：`x` 前进，`y` 左侧，`z` 向上

## 运动与约束参数

已配置以下关键参数：

1. 轮关节约束（`left_wheel_joint` / `right_wheel_joint`）
   - `type=continuous`
   - `effort=30.0`
   - `velocity=25.0`
   - `damping=0.2`
   - `friction=0.1`

2. 轮地接触参数（Gazebo）
   - `mu1=1.1`, `mu2=1.1`
   - `kp=100000`, `kd=5`
   - `minDepth=0.001`, `maxVel=0.5`

3. 差速驱动运动限制（Gazebo diff drive plugin）
   - `max_wheel_torque=30.0`
   - `max_wheel_acceleration=12.0`
   - 话题：`cmd_vel` / `odom`

## 注意事项

- 该模型是“仅两轮”结构，真实动力学下会存在侧翻风险。
- 如果你希望在 2D 平面稳定演示，可在仿真器里额外锁定 `z/roll/pitch` 自由度，或增加辅助支撑轮（caster）。
- 若你使用的是 Ignition/Gazebo Sim（非 Gazebo Classic），插件名和参数可能需要切换为对应版本。