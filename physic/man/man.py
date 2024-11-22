from manim import *
from manim.typing import Point3D

from physic.man.leg import Leg
from physic.physic_mobject import *
from character import Limb


class Man(object):

    def __init__(self, ground_height: Point3D) -> None:
        self.ground_height = ground_height
        self.head_radius = 1
        self.eye_radius = 0.15
        self.pupil_radius = 0.07
        self.body_height = 1.5
        self.body_height = 1.5
        self.body_width = 0.6
        self.head = PhysicalCircle(radius=self.head_radius, color=BLUE, fill_opacity=0.7)
        self.left_eye = Circle(radius=self.eye_radius, color=WHITE, fill_opacity=1).move_to(
            self.head.get_center() + LEFT * 0.4 + UP * 0.4)
        self.right_eye = Circle(radius=self.eye_radius, color=WHITE, fill_opacity=1).move_to(
            self.head.get_center() + RIGHT * 0.4 + UP * 0.4)
        self.left_pupil = Circle(radius=self.pupil_radius, color=BLACK, fill_opacity=1).move_to(
            self.left_eye.get_center() + LEFT * 0.05)
        self.right_pupil = Circle(radius=self.pupil_radius, color=BLACK, fill_opacity=1).move_to(
            self.right_eye.get_center())
        self.mouth = Line(start=LEFT * 0.4, end=RIGHT * 0.4, color=BLACK).move_to(
            self.head.get_center() + DOWN * 0.2)
        self.smile_mouth = Arc(radius=0.4, start_angle=-PI * 2 / 3, angle=PI / 2, color=BLACK)

        self.body = RoundedRectangle(width=self.body_width, height=self.body_height, color=BLUE, fill_opacity=0.7,
                                     corner_radius=0.3).move_to(
            self.head.get_center() + DOWN * (self.head_radius + self.body_height / 2 + 0.05))
        self.thigh_length = 1
        self.shin_length = 1
        self.left_arm = Limb(start=LEFT * 0.6, end=LEFT * 1.2 + DOWN * 0.5, is_left=True, color=BLUE).shift(DOWN * 1)
        self.right_arm = Limb(start=RIGHT * 0.6, end=RIGHT * 1.2 + DOWN * 0.5, is_left=False, color=BLUE).shift(
            DOWN * 1)
        self.left_leg = Leg(start=self.body.get_corner(DL) + RIGHT * 0.1, thigh_length=self.thigh_length,
                            shin_length=self.shin_length,
                            right=True, color=BLUE)
        self.right_leg = Leg(start=self.body.get_corner(DR) + LEFT * 0.1, thigh_length=self.thigh_length,
                             shin_length=self.shin_length,
                             right=False, color=BLUE)

        self.me = VGroup(self.head, self.left_eye, self.right_eye, self.left_pupil, self.right_pupil, self.mouth,
                         self.body, self.left_arm, self.right_arm, self.left_leg.it(), self.right_leg.it())
        drop = self.me.get_bottom() - ground_height
        if drop[1] != 0:
            self.me.move_to(self.me.get_center() + DOWN * drop[1])

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
        self.left_pupil.move_to(self.left_eye.get_center() + LEFT * 0.05)
        self.right_pupil.move_to(self.right_eye.get_center() + LEFT * 0.05)
        self.me.add_updater(self.body_walk_move_left)
        self.left_leg.walk_left()
        self.right_leg.walk_left()

    def stop_walk_left(self):
        self.left_pupil.move_to(self.left_eye.get_center())
        self.right_pupil.move_to(self.right_eye.get_center())
        self.me.remove_updater(self.body_walk_move_left)
        self.left_leg.stop_walk_left()
        self.right_leg.stop_walk_left()

    def walk_right(self):
        self.left_pupil.move_to(self.left_eye.get_center() + RIGHT * 0.05)
        self.right_pupil.move_to(self.right_eye.get_center() + RIGHT * 0.05)
        self.me.add_updater(self.body_walk_move_right)
        self.left_leg.walk_right()
        self.right_leg.walk_right()

    def stop_walk_right(self):
        self.left_pupil.move_to(self.left_eye.get_center())
        self.right_pupil.move_to(self.right_eye.get_center())
        self.me.remove_updater(self.body_walk_move_right)
        self.left_leg.stop_walk_right()
        self.right_leg.stop_walk_right()

    def stand_straight(self):
        self.left_leg.stand_straight()
        self.right_leg.stand_straight()

    def it(self):
        return self.me


class SceneA(Scene):
    def construct(self):
        screen_width = config.frame_width
        ground_line = Line(start=LEFT * (screen_width / 2), end=RIGHT * (screen_width / 2), color=GREY)
        ground_line.set_stroke(width=6)
        ground_line.shift(DOWN * 3)
        self.add(ground_line)

        main_role = Man(ground_line.get_bottom())

        body = main_role.it()
        body.move_to(
            ground_line.get_bottom() + UP * (body.get_top() - body.get_bottom()) / 2)
        self.play(FadeIn(body))

        main_role.walk_left()
        self.wait(4)
        main_role.stop_walk_left()
        main_role.stand_straight()
        self.wait(2)

        main_role.walk_right()
        self.wait(4)
        main_role.stop_walk_right()
        main_role.stand_straight()
        self.wait(2)



