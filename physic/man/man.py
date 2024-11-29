
from manim import Scene
from manim.typing import Vector3D
from typing_extensions import runtime

from physic.man.leg import Leg
from physic.physic_mobject import *
from physic.man.limb import Limb


class Man(object):

    def __init__(self, ground_height: Point3D, ratio: float=1) -> None:
        self.ground_height = ground_height
        self.head_radius = 1 * ratio
        self.eye_radius = 0.15 * ratio
        self.pupil_radius = 0.07 * ratio
        self.body_height = 1.5 * ratio
        self.body_height = 1.5 * ratio
        self.body_width = 0.6 * ratio
        self.thigh_length = 1 * ratio
        self.shin_length = 1 * ratio
        self.arm_length = 1 * ratio
        self.ratio = ratio
        self.bodies = []
        self.head = PhysicalCircle(radius=self.head_radius, color=BLUE, fill_opacity=1)

        self.left_eye_ball = Circle(radius=self.eye_radius, color=WHITE, fill_opacity=1).move_to(
            self.head.get_center() + LEFT * 0.4 * ratio + UP * 0.4 * ratio)
        self.left_pupil = Circle(radius=self.pupil_radius, color=BLACK, fill_opacity=1).move_to(
            self.left_eye_ball.get_center() + LEFT * 0.05 * ratio)
        self.left_eye = VGroup(self.left_eye_ball, self.left_pupil)

        self.right_eye_ball = Circle(radius=self.eye_radius, color=WHITE, fill_opacity=1).move_to(
            self.head.get_center() + RIGHT * 0.4 * ratio + UP * 0.4 * ratio)
        self.right_pupil = Circle(radius=self.pupil_radius, color=BLACK, fill_opacity=1).move_to(
            self.right_eye_ball.get_center() + RIGHT * 0.05 * ratio)
        self.right_eye = VGroup(self.right_eye_ball, self.right_pupil)

        self.mouth = Line(start=LEFT * 0.4 * ratio, end=RIGHT * 0.4 * ratio, color=BLACK).move_to(
            self.head.get_center() + DOWN * 0.2 * ratio)
        self.smile_mouth = Arc(radius=0.4 * ratio, start_angle=-PI * 2 / 3, angle=PI / 2, color=BLACK)

        self.body = PhysicalRoundedRectangle(width=self.body_width, height=self.body_height, color=BLUE, fill_opacity=0.7,
                                     corner_radius=0.3*ratio).move_to(
            self.head.get_center() + DOWN * (self.head_radius + self.body_height / 2 + 0.05))

        left_arm_start = self.body.get_corner(UL) + 0.1 * ratio * LEFT
        left_arm_end = left_arm_start + np.array([
            self.arm_length * np.cos((-1/2 -1/6) * np.pi),
            self.arm_length * np.sin((-1/2 -1/6) * np.pi),
            0
        ])
        self.left_arm = Limb(start=left_arm_start, end=left_arm_end, is_left=True, color=BLUE)

        right_arm_start = self.body.get_corner(UR) + 0.1 * ratio * RIGHT
        right_arm_end = right_arm_start + np.array([
            self.arm_length * np.cos((-1 / 2 + 1 / 6) * np.pi),
            self.arm_length * np.sin((-1 / 2 + 1 / 6) * np.pi),
            0
        ])
        self.right_arm = Limb(start=right_arm_start, end=right_arm_end, is_left=True, color=BLUE)
        self.left_leg = Leg(start=self.body.get_corner(DL) + RIGHT * 0.1 * ratio, thigh_length=self.thigh_length,
                            shin_length=self.shin_length,
                            right=True, color=BLUE)
        self.right_leg = Leg(start=self.body.get_corner(DR) + LEFT * 0.1 * ratio, thigh_length=self.thigh_length,
                             shin_length=self.shin_length,
                             right=False, color=BLUE)

        self.me = VGroup(self.head, self.left_eye, self.right_eye, self.mouth, self.body,
                         self.left_arm, self.right_arm, self.left_leg.it(), self.right_leg.it())
        drop = self.me.get_bottom() - ground_height
        if drop[1] != 0:
            self.me.move_to(self.me.get_center() + DOWN * drop[1])
        self.bodies.append(self.head)
        self.bodies.append(self.body)
        self.bodies.append(self.left_arm)
        self.bodies.append(self.right_arm)
        for body in self.left_leg.bodies:
            self.bodies.append(body)
        for body in self.right_leg.bodies:
            self.bodies.append(body)

    def face_front(self, s: Scene):
        left_arm_start = self.body.get_corner(UL) + 0.1 * self.ratio * LEFT
        left_arm_end = left_arm_start + np.array([
            self.arm_length * np.cos((-1 / 2 - 1 / 6) * np.pi),
            self.arm_length * np.sin((-1 / 2 - 1 / 6) * np.pi),
            0
        ])
        right_arm_start = self.body.get_corner(UR) + 0.1 * self.ratio * RIGHT
        right_arm_end = right_arm_start + np.array([
            self.arm_length * np.cos((-1 / 2 + 1 / 6) * np.pi),
            self.arm_length * np.sin((-1 / 2 + 1 / 6) * np.pi),
            0
        ])
        s.bring_to_back(self.head)
        s.play(
        self.left_pupil.animate.move_to(
            self.left_eye_ball.get_center() + LEFT * 0.05 * self.ratio),
            self.right_pupil.animate.move_to(
            self.right_eye_ball.get_center() + RIGHT * 0.05 * self.ratio),
            runtime=0.02
        )
        s.play(
            self.left_eye.animate.move_to(
                    self.head.get_center() + LEFT * 0.4 * self.ratio + UP * 0.4 * self.ratio),
            self.right_eye.animate.move_to(
                self.head.get_center() + RIGHT * 0.4 * self.ratio + UP * 0.4 * self.ratio),
            self.mouth.animate.put_start_and_end_on(start=self.head.get_center() + (DOWN * 0.2 + LEFT * 0.4) * self.ratio,
                                        end=self.head.get_center() + (DOWN * 0.2 + RIGHT * 0.4) * self.ratio),
            self.left_arm.animate.put_start_and_end_on(start=left_arm_start, end=left_arm_end),
            self.right_arm.animate.put_start_and_end_on(start=right_arm_start, end=right_arm_end),
            runtime=0.05
        )

    def face_back(self, s: Scene):
        s.bring_to_front(self.head)

    def turn(self, direction: Vector3D):
        if direction is not RIGHT and direction is not LEFT:
            return
        self.left_eye.move_to(
            self.head.get_center() + direction * 0.4 * self.ratio + UP * 0.4 * self.ratio)
        self.right_eye.move_to(
            self.head.get_center() + direction * 0.4 * self.ratio + UP * 0.4 * self.ratio)

        self.left_pupil.move_to(
            self.left_eye_ball.get_center() + direction * 0.05 * self.ratio)
        self.right_pupil.move_to(
            self.right_eye_ball.get_center() + direction * 0.05 * self.ratio)

        start_point = self.head.get_center() + DOWN * 0.2 * self.ratio + direction * 0.4 * self.ratio
        x0, y0, z0 = start_point
        cx, cy, _ = self.head.get_center()
        a = self.head_radius ** 2 - (y0 - cy) ** 2
        if a < 0:
            a = 0
        if direction is RIGHT:
            end_x = cx + np.sqrt(a)
        else:
            end_x = cx - np.sqrt(a)
        end_point = np.array([end_x, y0, 0])
        self.mouth.put_start_and_end_on(start_point, end_point)
        self.left_arm.put_start_and_end_on(start=self.body.get_corner(UP), end=self.body.get_corner(UP) + np.array([
            self.arm_length * np.cos((-1 / 2) * np.pi),
            self.arm_length * np.sin((-1 / 2) * np.pi),
            0
        ]))
        self.right_arm.put_start_and_end_on(start=self.body.get_corner(UP), end=self.body.get_corner(UP) + np.array([
            self.arm_length * np.cos((-1 / 2) * np.pi),
            self.arm_length * np.sin((-1 / 2) * np.pi),
            0
        ]))


    def turn_right(self):
        self.turn(RIGHT)

    def turn_left(self):
        self.turn(LEFT)

    def body_walk_move_left(self, obj, dt):
        angle = 0.01
        a = (self.thigh_length + self.shin_length) * np.sin(angle)
        obj.shift(LEFT * a)
        drop = obj.get_bottom() - self.ground_height
        if drop[1] > 0:
            obj.move_to(obj.get_center() + DOWN * drop[1])
        else:
            obj.move_to(obj.get_center() + DOWN * drop[1])

    def body_walk_move_right(self, obj, dt):
        angle = 0.01
        a = (self.thigh_length + self.shin_length) * np.sin(angle)
        obj.shift(RIGHT * a)
        drop = obj.get_bottom() - self.ground_height
        if drop[1] > 0:
            obj.move_to(obj.get_center() + DOWN * drop[1])
        else:
            obj.move_to(obj.get_center() + DOWN * drop[1])

    def walk_left(self):
        self.left_pupil.move_to(self.left_eye_ball.get_center() + LEFT * 0.05 * self.ratio)
        self.right_pupil.move_to(self.right_eye_ball.get_center() + LEFT * 0.05 * self.ratio)
        self.me.add_updater(self.body_walk_move_left)
        self.left_leg.walk_left()
        self.right_leg.walk_left()
        self.left_arm.start_walk()
        self.right_arm.start_walk()

    def stop_walk_left(self):
        self.left_pupil.move_to(self.left_eye_ball.get_center())
        self.right_pupil.move_to(self.right_eye_ball.get_center())
        self.me.remove_updater(self.body_walk_move_left)
        self.left_leg.stop_walk_left()
        self.right_leg.stop_walk_left()
        self.left_arm.stop_walk()
        self.right_arm.stop_walk()

    def walk_right(self):
        self.left_pupil.move_to(self.left_eye_ball.get_center() + RIGHT * 0.05 * self.ratio)
        self.right_pupil.move_to(self.right_eye_ball.get_center() + RIGHT * 0.05 * self.ratio)
        self.me.add_updater(self.body_walk_move_right)
        self.left_leg.walk_right()
        self.right_leg.walk_right()
        self.left_arm.start_walk()
        self.right_arm.start_walk()

    def stop_walk_right(self):
        self.left_pupil.move_to(self.left_eye_ball.get_center())
        self.right_pupil.move_to(self.right_eye_ball.get_center())
        self.me.remove_updater(self.body_walk_move_right)
        self.left_leg.stop_walk_right()
        self.right_leg.stop_walk_right()
        self.left_arm.stop_walk()
        self.right_arm.stop_walk()

    def stand_straight(self):
        self.left_leg.stand_straight()
        self.right_leg.stand_straight()

    def it(self):
        return self.me






