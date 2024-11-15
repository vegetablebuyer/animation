from manim import *
import numpy as np


class Leg(object):
    def __init__(self, left: bool=True):
        self.thigh_length = 2  # 大腿长度
        self.shin_length = 1.5  # 小腿长度
        self.hip_position = UP * 2  # 髋关节位置

        # 初始角度（弧度制）
        self.theta1 = -PI / 2  # 大腿与垂直线的初始夹角
        self.theta2 = -PI / 2  # 小腿与大腿的初始夹角

        # 动态角度变化范围
        self.theta1_min, self.theta1_max = -7 / 10 * PI, -3 / 10 * PI  # 大腿摆动范围

        # 动态角度更新速度
        speed = 0.05
        if left:
            self.theta1_speed = speed
        else:
            self.theta1_speed = -speed

        # 髋关节点
        self.hip = Dot(self.hip_position, color=BLUE)
        # 初始化大腿和小腿
        self.knee_position = self.hip.get_center() + np.array([
            self.thigh_length * np.cos(self.theta1),
            self.thigh_length * np.sin(self.theta1),
            0
        ])
        self.thigh = Line(
            self.hip.get_center(),
            self.knee_position,
            color=YELLOW
        )
        self.foot_position = self.knee_position + np.array([
            self.shin_length * np.cos(self.theta2),
            self.shin_length * np.sin(self.theta2),
            0
        ])
        self.shin = Line(
            self.knee_position,
            self.foot_position,
            color=GREEN
        )

        self.leg = VGroup(self.hip, self.thigh, self.shin)

    def walk_action(self, obj, dt):
        self.theta1 += self.theta1_speed
        if self.theta1 >= self.theta1_max or self.theta1 <= self.theta1_min:
            self.theta1_speed *= -1  # 摆动方向切换

        # 小腿角度规则
        swag_max = abs(PI/2 - abs(self.theta1_max))
        swag_min = abs(PI/2 - abs(self.theta1_min))
        if -PI / 2 <= self.theta1 <= -PI / 2 + swag_max / 2:
            self.theta2 = -PI / 2  # 小腿保持垂直
        elif -PI / 2 + swag_max / 2 < self.theta1 <= self.theta1_max:
            self.theta2 += 2 * self.theta1_speed
        elif -PI / 2 - swag_min / 2 <= self.theta1 < -PI / 2:
            self.theta2 += 2 * self.theta1_speed
        elif self.theta1_min <= self.theta1 < -PI / 2 - swag_min / 2:
            self.theta2 += self.theta1_speed

        # 更新膝盖位置（大腿末端）
        new_knee_position = self.hip.get_center() + np.array([
            self.thigh_length * np.cos(self.theta1),
            self.thigh_length * np.sin(self.theta1),
            0
        ])
        self.thigh.put_start_and_end_on(self.hip.get_center(), new_knee_position)

        # 更新脚位置（小腿末端）
        new_foot_position = new_knee_position + np.array([
            self.shin_length * np.cos(self.theta2),
            self.shin_length * np.sin(self.theta2),
            0
        ])
        self.shin.put_start_and_end_on(new_knee_position, new_foot_position)

    def walk(self):
        self.leg.add_updater(self.walk_action)

    def stop_walk(self):
        self.leg.remove_updater(self.walk_action)


class Walk(Scene):
    def construct(self):
        leg_a = Leg(left=False)
        leg_b = Leg(left=True)
        self.add(leg_a.leg)
        self.add(leg_b.leg)
        leg_a.leg.shift(LEFT*0.5)
        leg_b.walk()
        leg_a.walk()
        self.wait(10)
        leg_a.stop_walk()
        leg_b.stop_walk()
