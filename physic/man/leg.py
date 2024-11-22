
from physic.physic_mobject import *



class Leg(VMobject):
    def __init__(self, start: Point3D, thigh_length: int = 1, shin_length: int = 0.5,
                 right: bool = True, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.thigh_length = thigh_length  # thigh length
        self.shin_length = shin_length  # shin length
        # initial angle
        self.thigh_angle = -PI / 2  # thigh initial angle
        self.shin_angle = -PI / 2  # shin initial angle

        # thigh swag range
        self.thigh_angle_min, self.thigh_angle_max = (-PI / 2) - (PI / 7), (-PI / 2) + (PI / 7)  # 大腿摆动范围
        self.bodies = []
        # thigh swag speed
        speed = 0.02
        if right:
            self.swag_speed = speed
        else:
            self.swag_speed = -speed
        self.hip = Dot(point=start, radius=0, *args, **kwargs)
        self.knee_position = self.hip.get_center() + np.array([
            self.thigh_length * np.cos(self.thigh_angle),
            self.thigh_length * np.sin(self.thigh_angle),
            0
        ])
        self.thigh = PhysicalLine(
            self.hip.get_center(),
            self.knee_position,
            *args, **kwargs
        )
        self.bodies.append(self.thigh)
        self.foot_position = self.knee_position + np.array([
            self.shin_length * np.cos(self.shin_angle),
            self.shin_length * np.sin(self.shin_angle),
            0
        ])
        self.shin = PhysicalLine(
            self.knee_position,
            self.foot_position,
            *args, **kwargs
        )
        self.bodies.append(self.shin)
        self.leg = VGroup(self.hip, self.thigh, self.shin)
        self.walk_left_func = lambda mob, dt: self.walk_action(mob, dt, position=LEFT)
        self.walk_right_func = lambda mob, dt: self.walk_action(mob, dt, position=RIGHT)

    def it(self):
        return self.leg

    def shin_right_action(self):
        swag_max = abs(PI / 2 - abs(self.thigh_angle_max))
        swag_min = abs(PI / 2 - abs(self.thigh_angle_min))
        if -PI / 2 <= self.thigh_angle <= -PI / 2 + swag_max / 2:
            # shin keep straight
            self.shin_angle = -PI / 2
        elif -PI / 2 + swag_max / 2 < self.thigh_angle <= self.thigh_angle_max:
            self.shin_angle += 2 * self.swag_speed
        elif -PI / 2 - swag_min / 2 <= self.thigh_angle < -PI / 2:
            self.shin_angle += 2 * self.swag_speed
        elif self.thigh_angle_min <= self.thigh_angle < -PI / 2 - swag_min / 2:
            self.shin_angle += self.swag_speed

    def shin_left_action(self):
        swag_max = abs(PI / 2 - abs(self.thigh_angle_max))
        swag_min = abs(PI / 2 - abs(self.thigh_angle_min))
        if -PI / 2 - swag_max / 2 <= self.thigh_angle <= -PI / 2:
            # shin keep straight
            self.shin_angle = -PI / 2
        elif self.thigh_angle_max < self.thigh_angle <= -PI / 2 - swag_max / 2:
            self.shin_angle += 2 * self.swag_speed
        elif -PI / 2 <= self.thigh_angle < -PI / 2 + swag_min / 2:
            self.shin_angle += 2 * self.swag_speed
        elif -PI / 2 + swag_min / 2 <= self.thigh_angle < self.thigh_angle_min:
            self.shin_angle += self.swag_speed

    def set_position(self):
        new_knee_position = self.hip.get_center() + np.array([
            self.thigh_length * np.cos(self.thigh_angle),
            self.thigh_length * np.sin(self.thigh_angle),
            0
        ])
        self.thigh.phy_put_start_and_end_on(self.hip.get_center(), new_knee_position)

        # update foot position
        new_foot_position = new_knee_position + np.array([
            self.shin_length * np.cos(self.shin_angle),
            self.shin_length * np.sin(self.shin_angle),
            0
        ])
        self.shin.phy_put_start_and_end_on(new_knee_position, new_foot_position)

    def walk_action(self, obj, dt, position):
        self.thigh_angle += self.swag_speed
        if self.thigh_angle >= self.thigh_angle_max or self.thigh_angle <= self.thigh_angle_min:
            # change the swag direction
            self.swag_speed *= -1
        if position is RIGHT:
            self.shin_right_action()
        elif position is LEFT:
            self.shin_left_action()
        else:
            return
        self.set_position()

    def walk_right(self):
        self.leg.add_updater(self.walk_right_func)

    def stop_walk_right(self):
        self.leg.remove_updater(self.walk_right_func)

    def walk_left(self):
        self.leg.add_updater(self.walk_left_func)

    def stop_walk_left(self):
        self.leg.remove_updater(self.walk_left_func)

    def stand_straight_func(self, obj, dt):
        if (((-PI / 2 - abs(self.swag_speed)) <= self.thigh_angle <= (-PI / 2 + abs(self.swag_speed))) and
                ((-PI / 2 - abs(self.swag_speed)) <= self.shin_angle <= (-PI / 2 + abs(self.swag_speed)))):
            self.leg.remove_updater(self.stand_straight_func)
            return
        if self.thigh_angle < -PI / 2:
            self.thigh_angle += abs(self.swag_speed / 2)
        elif self.thigh_angle > -PI / 2:
            self.thigh_angle -= abs(self.swag_speed / 2)
        if self.shin_angle < -PI / 2:
            self.shin_angle += abs(self.swag_speed / 2)
        elif self.shin_angle > -PI / 2:
            self.shin_angle -= abs(self.swag_speed / 2)
        self.set_position()

    def stand_straight(self):
        self.leg.add_updater(self.stand_straight_func)


class Walk(Scene):
    def construct(self):
        left_leg = Leg(start=UP * 2, right=False)
        right_leg = Leg(start=UP * 2, right=True)
        self.add(left_leg.leg)
        self.add(right_leg.leg)
        left_leg.leg.shift(LEFT * 0.5)
        left_leg.walk_right()
        right_leg.walk_right()
        self.wait(3.5)
        left_leg.stop_walk_right()
        right_leg.stop_walk_right()
        left_leg.stand_straight()
        right_leg.stand_straight()
        self.wait(2)
        left_leg.walk_left()
        right_leg.walk_left()
        self.wait(3.5)
        left_leg.stop_walk_left()
        right_leg.stop_walk_left()
        left_leg.stand_straight()
        right_leg.stand_straight()
        self.wait(2)
        # left_leg.walk_left()
        # right_leg.walk_left()
        # self.wait(10)
        # left_leg.stop_walk_left()
        # right_leg.stop_walk_left()

