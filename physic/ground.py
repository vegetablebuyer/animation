from manim import *
import pymunk

class PhysicalGround(Line):
    def __init__(self, y_pos: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)

        self.shape = pymunk.Segment(self.body, (-10, y_pos), (10, y_pos), 0.1)
        self.shape.elasticity = 1
        self.shape.collision_type = 2
        self.shift(y_pos * UP)