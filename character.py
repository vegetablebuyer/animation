from manim import *
from manim.typing import Point3D
import numpy as np


class Limb(Line):

    def __init__(self, start: Point3D, end: Point3D, **kwargs):
        super().__init__(start=start, end=end, **kwargs)
        self.start_angle = np.arctan2(end[1] - start[1], end[0] - start[0])
        if -PI/2 <= self.start_angle <= PI/2:
            self.end_angle = PI - self.start_angle
        else:
            self.end_angle = -PI - self.start_angle
        self.add = True
        self.need = True

    def wave(self, obj, dt):
        print("xxxx", self.add)
        step = 0.05
        start = obj.get_start()
        end = obj.get_end()
        angle = np.arctan2(end[1] - start[1], end[0] - start[0])
        if 0 <= self.start_angle < np.pi / 2 or -np.pi <= self.start_angle < -np.pi / 2:
            # first quadrant and third quadrant
            if angle <= self.start_angle:
                self.add = True
                obj.rotate(step, about_point=obj.get_start())
                return
            elif angle >= self.end_angle:
                self.add = False
                obj.rotate(-step, about_point=obj.get_start())
                return
        elif np.pi / 2 <= self.start_angle < np.pi or -np.pi / 2 <= self.start_angle < 0:
            # second quadrant and fourth quadrant
            if angle >= self.start_angle:
                self.add = False
                obj.rotate(-step, about_point=obj.get_start())
                return
            elif angle <= self.end_angle:
                self.add = True
                obj.rotate(step, about_point=obj.get_start())
                return

        if self.add:
            obj.rotate(step, about_point=obj.get_start())
        elif not self.add:
            obj.rotate(-step, about_point=obj.get_start())


    def walk(self):
        self.add_updater(self.wave)

    def stop_walk(self):
        self.remove_updater(self.wave)


class Robot(object):
    def __init__(self):
        self.head_radius = 1
        self.eye_radius = 0.15
        self.pupil_radius = 0.07
        self.body_height = 1.5
        self.body_width = 0.6
        self.head = Circle(radius=self.head_radius, color=GREEN, fill_opacity=0.7)
        self.left_eye = Circle(radius=self.eye_radius, color=WHITE, fill_opacity=1).move_to(
            self.head.get_center() + LEFT * 0.4 + UP * 0.4)
        self.right_eye = Circle(radius=self.eye_radius, color=WHITE, fill_opacity=1).move_to(
            self.head.get_center() + RIGHT * 0.4 + UP * 0.4)
        self.left_pupil = Circle(radius=self.pupil_radius, color=BLACK, fill_opacity=1).move_to(
            self.left_eye.get_center() + LEFT * 0.05)
        self.right_pupil = Circle(radius=self.pupil_radius, color=BLACK, fill_opacity=1).move_to(
            self.right_eye.get_center() + LEFT * 0.05)
        self.mouth = Line(start=LEFT * 0.4, end=RIGHT * 0.4, color=BLACK).move_to(
            self.head.get_center() + DOWN * 0.2)
        self.smile_mouth = Arc(radius=0.4, start_angle=-PI * 2 / 3, angle=PI / 2, color=BLACK)

        self.body = RoundedRectangle(width=self.body_width, height=self.body_height, color=BLUE, fill_opacity=0.7, corner_radius=0.3).move_to(
            self.head.get_center() + DOWN * (self.head_radius + self.body_height/2 + 0.05))

        self.left_arm = Limb(start=LEFT * 0.6, end=LEFT * 1.2 + DOWN * 0.5, color=BLUE).shift(DOWN * 1)
        self.right_arm = Limb(start=RIGHT * 0.6, end=RIGHT * 1.2 + DOWN * 0.5, color=BLUE).shift(DOWN * 1)
        self.left_leg = Limb(start=DOWN * 2.5, end=LEFT * 0.5 + DOWN * 3.5, color=BLUE)
        self.right_leg = Limb(start=DOWN * 2.5, end=RIGHT * 0.5 + DOWN * 3.5, color=BLUE)

        self.me = VGroup(self.head, self.left_eye, self.right_eye, self.left_pupil, self.right_pupil, self.mouth,
                         self.body, self.left_arm, self.right_arm, self.left_leg, self.right_leg)

    def it(self):
        return self.me

    def smile(self):
        self.smile_mouth.shift(self.mouth.get_center())
        return Transform(self.mouth, self.smile_mouth, run_time=2)

    def move_to_center(self):
        return self.me.animate.move_to(ORIGIN)

    def jump_up(self):
        return self.me.animate.shift(UP * 0.5)

    def jump_down(self):
        return self.me.animate.shift(DOWN * 0.5)

    def rotate_eye_pupil(self):
        play1 = Rotate(self.left_pupil, angle=2 * TAU, about_point=self.left_eye.get_center(), run_time=4)
        play2 = Rotate(self.right_pupil, angle=2 * TAU, about_point=self.right_eye.get_center(), run_time=4)
        return play1, play2


    def walk(self):
        self.left_leg.walk()
        self.right_leg.walk()

    def stop_walk(self):
        self.left_leg.stop_walk()
        self.right_leg.stop_walk()


class CartoonCharacter(Scene):
    def construct(self):
        screen_width = config.frame_width
        screen_height = config.frame_height

        main_role = Robot()
        # role enter the scene
        main_role.it().move_to(ORIGIN + RIGHT * (screen_width / 2))

        self.play(FadeIn(main_role.it()))

        # make the role walk to the center of the scene
        main_role.walk()
        self.play(main_role.move_to_center(), run_time=5)

        main_role.stop_walk()

        # role smile and rotate the eyeball
        self.play(main_role.rotate_eye_pupil(), main_role.smile())
        # role jump
        self.play(main_role.jump_up(), run_time=0.5)
        self.play(main_role.jump_down(), run_time=0.5)

        # role exit the scene
        self.play(FadeOut(main_role.it()))
