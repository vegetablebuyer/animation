from manim import *
from manim.typing import Point3D
import pymunk
import random

from physic.ground import PhysicalGround
from physic.space import PhysicalSpace
from physic.rain import RainDrop, collision_handle
from physic.man.man import Man


class RainScene(Scene):
    def construct(self):
        space = PhysicalSpace(self, 1 / config.frame_rate)
        self.add(space)
        ground = PhysicalGround(y_pos=-3, start=LEFT * 10, end=RIGHT * 10, color=GREY)
        self.add(ground)

        space.add_body(ground)
        rain = RainDrop(color=WHITE)
        handler = space.register_collision_event(rain.shape.collision_type, ground.shape.collision_type)

        collision_handle(handler)

        def add_random_raindrop(dt):
            for _ in range(5):

                rain = RainDrop(color=WHITE)
                self.add(rain.rain)
                space.add_body(rain)

        self.add_updater(add_random_raindrop)
        self.wait(5)
        self.remove_updater(add_random_raindrop)
        self.wait(2)

class SceneA(Scene):
    def construct(self):
        space = PhysicalSpace(self, 1 / config.frame_rate)
        self.add(space)
        ground = PhysicalGround(y_pos=-3, start=LEFT * 10, end=RIGHT * 10, color=GREY)
        ground.set_stroke(width=6)
        self.add(ground)
        space.add_body(ground)


        main_role = Man(ground.get_bottom())
        space.add_body(*main_role.bodies)

        rain = RainDrop(color=WHITE)
        handler = space.register_collision_event(rain.shape.collision_type, ground.shape.collision_type)

        collision_handle(handler)

        def add_random_raindrop(dt):
            for _ in range(10):
                rain = RainDrop(color=WHITE)
                self.add(rain.rain)
                space.add_body(rain)

        self.add_updater(add_random_raindrop)
        body = main_role.it()
        body.move_to(
            ground.get_bottom() + UP * (body.get_top() - body.get_bottom()) / 2)
        self.play(FadeIn(body))

        main_role.walk_left()
        self.wait(8)

        main_role.stop_walk_left()
        main_role.stand_straight()
        self.wait(2)

        main_role.walk_right()
        self.wait(8)
        main_role.stop_walk_right()
        main_role.stand_straight()
        self.wait(2)
        self.remove_updater(add_random_raindrop)

