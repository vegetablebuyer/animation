from manim import *
import pymunk
from manim.typing import Point3D


class PhysicalGround(Line):
    def __init__(self, start: Point3D, end: Point3D, y_pos: int = 0,  **kwargs):
        start +=  UP * y_pos
        end += UP * y_pos
        super().__init__(start=start, end=end, **kwargs)
        start_pos = (start[0], start[1])
        end_pos = (end[0] - start[0], end[1] - start[1])
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = start_pos

        self.shape = pymunk.Segment(self.body, (0, 0), end_pos, 0.1)
        self.shape.elasticity = 1
        self.shape.collision_type = 2


# ground = Ground(y_pos=-3, start=LEFT * 10, end=RIGHT * 10, color=GREY)