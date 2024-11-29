from manim import *

from physic.man.man import Man
from physic.ground import PhysicalGround
from physic.space import PhysicalSpace

class TestMan(MovingCameraScene):
    def construct(self):

        # self.camera.background_color = GREEN
        space = PhysicalSpace(self, 1 / config.frame_rate)
        self.add(space)
        ground = PhysicalGround(y_pos=-2, start=LEFT * 10, end=RIGHT * 10)
        self.add(ground.line)
        self.add(ground.land)
        space.add_body(*ground.bodies)
        space.add_shape(*ground.shapes)

        default_handler = space.space.add_default_collision_handler()
        default_handler.begin = lambda arbiter, space, data: False

        main_role = Man(ground.line.get_bottom() -1 , 0.5)
        space.add_body_and_shape(*main_role.bodies)

        body = main_role.it()
        self.play(FadeIn(body))

        main_role.turn_right()
        self.wait(2)
        main_role.turn_left()
        self.wait(2)

        main_role.walk_left()
        self.wait(2)

        main_role.stop_walk_left()
        main_role.stand_straight()
        self.wait(2)
        main_role.face_front(self)
        self.wait(2)
        main_role.face_back(self)
        self.wait(2)
        main_role.face_front(self)
        self.wait(2)