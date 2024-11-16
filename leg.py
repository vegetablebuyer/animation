from manim import *
import numpy as np


class Leg(object):
    def __init__(self, right: bool=True):
        self.thigh_length = 2  # thigh length
        self.shin_length = 1.5  # shin length
        self.hip_position = UP * 2  # start position of the thigh

        # initial angle
        self.thigh_angle = -PI / 2  # thigh initial angle
        self.shin_angle = -PI / 2  # shin initial angle

        # thigh swag range
        self.thigh_angle_min, self.thigh_angle_max = (-PI/2)- (PI/5), (-PI/2)+ (PI/5)  # 大腿摆动范围

        # thigh swag speed
        speed = 0.05
        if right:
            self.swag_speed = speed
        else:
            self.swag_speed = -speed

        
        self.hip = Dot(self.hip_position, color=BLUE)

        self.knee_position = self.hip.get_center() + np.array([
            self.thigh_length * np.cos(self.thigh_angle),
            self.thigh_length * np.sin(self.thigh_angle),
            0
        ])
        self.thigh = Line(
            self.hip.get_center(),
            self.knee_position,
            color=YELLOW
        )
        self.foot_position = self.knee_position + np.array([
            self.shin_length * np.cos(self.shin_angle),
            self.shin_length * np.sin(self.shin_angle),
            0
        ])
        self.shin = Line(
            self.knee_position,
            self.foot_position,
            color=GREEN
        )

        self.leg = VGroup(self.hip, self.thigh, self.shin)

    def walk_right_action(self, obj, dt):
        self.thigh_angle += self.swag_speed
        if self.thigh_angle >= self.thigh_angle_max or self.thigh_angle <= self.thigh_angle_min:
            # change the swag direction
            self.swag_speed *= -1

        swag_max = abs(PI/2 - abs(self.thigh_angle_max))
        swag_min = abs(PI/2 - abs(self.thigh_angle_min))
        if -PI / 2 <= self.thigh_angle <= -PI / 2 + swag_max / 2:
            # shin keep straight
            self.shin_angle = -PI / 2
        elif -PI / 2 + swag_max / 2 < self.thigh_angle <= self.thigh_angle_max:
            self.shin_angle += 2 * self.swag_speed
        elif -PI / 2 - swag_min / 2 <= self.thigh_angle < -PI / 2:
            self.shin_angle += 2 * self.swag_speed
        elif self.thigh_angle_min <= self.thigh_angle < -PI / 2 - swag_min / 2:
            self.shin_angle += self.swag_speed

        # update knee position
        new_knee_position = self.hip.get_center() + np.array([
            self.thigh_length * np.cos(self.thigh_angle),
            self.thigh_length * np.sin(self.thigh_angle),
            0
        ])
        self.thigh.put_start_and_end_on(self.hip.get_center(), new_knee_position)

       # update foot position
        new_foot_position = new_knee_position + np.array([
            self.shin_length * np.cos(self.shin_angle),
            self.shin_length * np.sin(self.shin_angle),
            0
        ])
        self.shin.put_start_and_end_on(new_knee_position, new_foot_position)

    def walk_left_action(self, obj, dt):
        
        self.thigh_angle += self.swag_speed
        if self.thigh_angle >= self.thigh_angle_max or self.thigh_angle <= self.thigh_angle_min:
            # change the swag direction
            self.swag_speed *= -1 

        swag_max = abs(PI/2 - abs(self.thigh_angle_max))
        swag_min = abs(PI/2 - abs(self.thigh_angle_min))
        if -PI /2 - swag_max /2 <= self.thigh_angle <= -PI/2:
            # shin keep straight
            self.shin_angle = -PI / 2 
        elif self.thigh_angle_max < self.thigh_angle <= -PI /2 - swag_max /2:
            self.shin_angle += 2 * self.swag_speed
        elif  -PI / 2 <= self.thigh_angle < -PI / 2 + swag_min / 2:
            self.shin_angle += 2 * self.swag_speed
        elif -PI / 2 + swag_min / 2 <= self.thigh_angle < self.thigh_angle_min:
            self.shin_angle += self.swag_speed

        # update knee position
        new_knee_position = self.hip.get_center() + np.array([
            self.thigh_length * np.cos(self.thigh_angle),
            self.thigh_length * np.sin(self.thigh_angle),
            0
        ])
        self.thigh.put_start_and_end_on(self.hip.get_center(), new_knee_position)

        # update foot position
        new_foot_position = new_knee_position + np.array([
            self.shin_length * np.cos(self.shin_angle),
            self.shin_length * np.sin(self.shin_angle),
            0
        ])
        self.shin.put_start_and_end_on(new_knee_position, new_foot_position)

    def walk_right(self):
        self.leg.add_updater(self.walk_right_action)

    def stop_walk_right(self):
        self.leg.remove_updater(self.walk_right_action)

    def walk_left(self):
        self.leg.add_updater(self.walk_left_action)

    def stop_walk_left(self):
        self.leg.remove_updater(self.walk_left_action)


class Walk(Scene):
    def construct(self):
        left_leg = Leg(right=False)
        right_leg = Leg(right=True)
        self.add(left_leg.leg)
        self.add(right_leg.leg)
        left_leg.leg.shift(LEFT*0.5)
        left_leg.walk_right()
        right_leg.walk_right()
        self.wait(10)
        left_leg.stop_walk_right()
        right_leg.stop_walk_right()
        # left_leg.walk_left()
        # right_leg.walk_left()
        # self.wait(10)
        # left_leg.stop_walk_left()
        # right_leg.stop_walk_left()

