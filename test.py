from manim import *
from manim.typing import Point3D
import pymunk
import random

from physic.ground import PhysicalGround
from physic.space import PhysicalSpace
from physic.rain import RainDrop, collision_handle


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
        self.wait(15)
        self.remove_updater(add_random_raindrop)
        self.wait(2)

