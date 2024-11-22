from manim import *

from physic.space import PhysicalSpace
from physic.ground import PhysicalGround
from physic.rain import RainDrop, collision_handle
from physic.man.leg import Leg


class A(Scene):
    def construct(self):
        space = PhysicalSpace(self, 1 / config.frame_rate)
        self.add(space)
        ground = PhysicalGround(y_pos=-3, start=LEFT * 10, end=RIGHT * 10, color=GREY)
        self.add(ground)

        left_leg = Leg(start=UP * 2, right=False, color=BLUE)
        self.add(left_leg.leg)

        space.add_body(ground)
        space.add_body(*left_leg.bodies)
        rain = RainDrop(color=WHITE)
        handler = space.register_collision_event(rain.shape.collision_type, ground.shape.collision_type)

        collision_handle(handler)

        def add_random_raindrop(dt):
            for _ in range(10):

                rain = RainDrop(color=WHITE)
                self.add(rain.rain)
                space.add_body(rain)

        self.add_updater(add_random_raindrop)
        self.wait(5)
        left_leg.walk_right()
        self.wait(10)
        left_leg.stop_walk_right()
        self.wait(5)
        self.remove_updater(add_random_raindrop)
        self.wait(2)