#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import select
import termios
import tty
from typing import Dict, List, Tuple

import rospy
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


def build_help_text(key_to_action: Dict[str, Tuple[str, float]], reset_key: str, help_key: str, exit_key: str) -> str:
    lines = [
        "W2A Arm Keyboard Teleop (Param Driven)",
        "====================================",
        "按键映射（由参数 key_bindings 定义）:",
    ]

    for key in sorted(key_to_action.keys()):
        joint, delta = key_to_action[key]
        sign = "+" if delta >= 0 else "-"
        lines.append(f"  {key:<3} : {joint} {sign}{abs(delta):g}*step")

    lines.extend(
        [
            "",
            f"  {reset_key:<3} : 全部关节回零",
            f"  {help_key:<3} : 打印帮助",
            f"  {exit_key:<3} : 退出程序",
            "",
            "注意:",
            "- 需要先启动 w2a 仿真并加载 arm_joint_controller",
            "- 本节点发布到 /arm_joint_controller/command (JointTrajectory)",
        ]
    )

    return "\n".join(lines)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


class ArmKeyboardTeleop:
    def __init__(self) -> None:
        self.joint_names: List[str] = rospy.get_param(
            "~joint_names",
            ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5"],
        )
        self.step_rad: float = float(rospy.get_param("~step_rad", 0.08))
        self.trajectory_time: float = float(rospy.get_param("~trajectory_time", 0.45))
        self.command_topic: str = rospy.get_param("~command_topic", "/arm_joint_controller/command")
        self.joint_state_topic: str = rospy.get_param("~joint_state_topic", "/joint_states")
        self.reset_key: str = str(rospy.get_param("~reset_key", "z"))
        self.help_key: str = str(rospy.get_param("~help_key", "h"))
        self.exit_key: str = str(rospy.get_param("~exit_key", "x"))

        self.joint_limits_raw: Dict[str, List[float]] = rospy.get_param("~joint_limits", {})
        self.joint_limits: Dict[str, Tuple[float, float]] = {}
        for j in self.joint_names:
            bounds = self.joint_limits_raw.get(j, [-3.14, 3.14])
            self.joint_limits[j] = (float(bounds[0]), float(bounds[1]))

        self.current_targets: Dict[str, float] = {j: 0.0 for j in self.joint_names}
        self.has_joint_state = False

        self.pub = rospy.Publisher(self.command_topic, JointTrajectory, queue_size=5)
        self.sub = rospy.Subscriber(self.joint_state_topic, JointState, self._joint_state_cb, queue_size=5)

        raw_bindings = rospy.get_param("~key_bindings", {})
        self.key_to_action: Dict[str, Tuple[str, float]] = {}
        for key, cfg in raw_bindings.items():
            if not isinstance(cfg, dict):
                rospy.logwarn("忽略无效键位配置 %r: %r", key, cfg)
                continue
            joint = cfg.get("joint")
            delta = float(cfg.get("delta", 0.0))
            if joint not in self.joint_names:
                rospy.logwarn("忽略键位 %r，joint=%r 不在 joint_names 中", key, joint)
                continue
            if delta == 0.0:
                rospy.logwarn("忽略键位 %r，delta=0 没有意义", key)
                continue
            self.key_to_action[str(key)] = (str(joint), delta)

        if not self.key_to_action:
            rospy.logwarn("未提供有效 key_bindings，启用默认映射。")
            self.key_to_action = {
                "1": ("joint_1", +1.0), "q": ("joint_1", -1.0),
                "2": ("joint_2", +1.0), "w": ("joint_2", -1.0),
                "3": ("joint_3", +1.0), "e": ("joint_3", -1.0),
                "4": ("joint_4", +1.0), "r": ("joint_4", -1.0),
                "5": ("joint_5", +1.0), "t": ("joint_5", -1.0),
            }

        self.help_text = build_help_text(self.key_to_action, self.reset_key, self.help_key, self.exit_key)

    def _joint_state_cb(self, msg: JointState) -> None:
        if not msg.name or not msg.position:
            return
        name_to_pos = dict(zip(msg.name, msg.position))
        updated = False
        for j in self.joint_names:
            if j in name_to_pos:
                self.current_targets[j] = float(name_to_pos[j])
                updated = True
        if updated:
            self.has_joint_state = True

    def _publish_targets(self) -> None:
        jt = JointTrajectory()
        jt.joint_names = list(self.joint_names)

        point = JointTrajectoryPoint()
        point.positions = [self.current_targets[j] for j in self.joint_names]
        point.time_from_start = rospy.Duration.from_sec(self.trajectory_time)

        jt.points = [point]
        self.pub.publish(jt)

    def _apply_step(self, joint_name: str, delta_scale: float) -> None:
        low, high = self.joint_limits[joint_name]
        raw_value = self.current_targets[joint_name] + delta_scale * self.step_rad
        self.current_targets[joint_name] = clamp(raw_value, low, high)

    def print_state(self) -> None:
        ordered = [f"{j}={self.current_targets[j]:+.2f}" for j in self.joint_names]
        rospy.loginfo("targets: %s", " | ".join(ordered))

    def run(self) -> None:
        settings = termios.tcgetattr(sys.stdin)

        try:
            rospy.loginfo("\n%s", self.help_text)
            rospy.loginfo("等待 /joint_states 初始化（2秒超时后继续）...")

            t0 = rospy.Time.now()
            while (not rospy.is_shutdown()) and (not self.has_joint_state):
                if (rospy.Time.now() - t0).to_sec() > 2.0:
                    rospy.logwarn("未收到 /joint_states，使用默认零位继续。")
                    break
                rospy.sleep(0.05)

            self.print_state()
            self._publish_targets()

            while not rospy.is_shutdown():
                tty.setraw(sys.stdin.fileno())
                rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                key = sys.stdin.read(1) if rlist else ""
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

                if not key:
                    continue

                if key in self.key_to_action:
                    joint_name, delta_scale = self.key_to_action[key]
                    self._apply_step(joint_name, delta_scale)
                    self._publish_targets()
                    self.print_state()
                elif key == self.reset_key:
                    for j in self.joint_names:
                        self.current_targets[j] = 0.0
                    self._publish_targets()
                    rospy.loginfo("全部关节已回零。")
                    self.print_state()
                elif key == self.help_key:
                    rospy.loginfo("\n%s", self.help_text)
                elif key == self.exit_key or key == "\x03":
                    rospy.loginfo("退出键盘控臂。")
                    break
                else:
                    rospy.loginfo("未绑定按键: %r（按 h 查看帮助）", key)

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


def main() -> None:
    rospy.init_node("arm_keyboard_teleop", anonymous=False)
    teleop = ArmKeyboardTeleop()
    teleop.run()


if __name__ == "__main__":
    main()
