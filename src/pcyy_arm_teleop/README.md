# pcyy_arm_teleop（机械臂参数映射版）

仅保留机械臂 5 关节控制：`joint_1 ~ joint_5`。

实现方式参考 `rqt_joint_trajectory_controller`：
- `rqt` 本质是调节各关节目标位置；
- 本包将“按键”映射为“目标位置增量”（通过参数 `key_bindings`）；
- 所有重映射都在 `config/arm_teleop.yaml` 中完成，无需改代码。

## 一键运行

在工作空间根目录执行：

`./run_arm_only.sh`

## 按键

- 默认键位在 `config/arm_teleop.yaml` 的 `key_bindings`。
- 例如：`"1": {joint: joint_1, delta: 1}` 表示按 `1` 执行 `joint_1 += step_rad`。
- 特殊键也可参数化：`reset_key`、`help_key`、`exit_key`。
