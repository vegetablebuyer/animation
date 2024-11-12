from manim import *


class Robot(object):
    def __init__(self):
        self.head_radius = 1
        self.eye_radius = 0.15
        self.pupil_radius = 0.07
        self.body_height = 1.5
        self.body_width = 0.6
        self.head = Circle(radius=self.head_radius, color=BLUE, fill_opacity=0.7)
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

        self.left_arm = Line(start=LEFT * 0.6, end=LEFT * 1.2 + DOWN * 0.5, color=BLUE).shift(DOWN * 1)
        self.right_arm = Line(start=RIGHT * 0.6, end=RIGHT * 1.2 + DOWN * 0.5, color=BLUE).shift(DOWN * 1)
        self.left_leg = Line(start=DOWN * 2.5, end=LEFT * 0.5 + DOWN * 3.5, color=BLUE)
        self.right_leg = Line(start=DOWN * 2.5, end=RIGHT * 0.5 + DOWN * 3.5, color=BLUE)

        self.me = VGroup(self.head, self.left_eye, self.right_eye, self.left_pupil, self.right_pupil, self.mouth,
                         self.body, self.left_arm, self.right_arm, self.left_leg, self.right_leg)

    def it(self):
        return self.me

    def smile(self):
        self.smile_mouth.shift(self.mouth.get_center())
        return Transform(self.mouth, self.smile_mouth, run_time=2)

    def move_to_center(self):
        return self.me.animate.shift(RIGHT * 2)

    def jump_up(self):
        return self.me.animate.shift(UP * 0.5)

    def jump_down(self):
        return self.me.animate.shift(DOWN * 0.5)

    def rotate_eye_pupil(self):
        play1 = Rotate(self.left_pupil, angle=2 * TAU, about_point=self.left_eye.get_center(), run_time=4)
        play2 = Rotate(self.right_pupil, angle=2 * TAU, about_point=self.right_eye.get_center(), run_time=4)
        return play1, play2

    def walk(self):
        down = True
        for _ in range(6):
            if down:
                down = False
                yield [self.left_leg.animate.shift(DOWN * 0.1 + LEFT * 0.1),
                       self.right_leg.animate.shift(DOWN * 0.1 + RIGHT * 0.1)]
            else:
                down = True
                yield [self.left_leg.animate.shift(UP * 0.1 + RIGHT * 0.1),
                       self.right_leg.animate.shift(UP * 0.1 + LEFT * 0.1)]


class CartoonCharacter(Scene):
    def construct(self):

        main_role = Robot()
        # role enter the scene
        self.play(FadeIn(main_role.it()))

        # move the role to the center of the scene
        self.play(main_role.move_to_center(), run_time=2)

        # role smile and rotate the eye ball
        self.play(main_role.rotate_eye_pupil(), main_role.smile())

        # role jump
        self.play(main_role.jump_up(), run_time=0.5)
        self.play(main_role.jump_down(), run_time=0.5)

        # role walk
        for animations in main_role.walk():
            self.play(animations, run_time=0.2)
        # role exit the scene
        self.play(FadeOut(main_role.it()))
