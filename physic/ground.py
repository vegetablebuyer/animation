from manim import *
from manim.utils.color.XKCD import BROWN
import pymunk
from manim.typing import Point3D


class PhysicalGround(object):
    def __init__(self, start: Point3D, end: Point3D, y_pos: int = 0,  **kwargs):

        self.bodies = []
        self.shapes = []
        self.collision_type_list = []
        for i in range(0, int(y_pos + abs(config.frame_height / 2)) + 1 ):
            y = y_pos - i
            _start = start + UP * y
            _end = end + UP * y
            start_pos = (_start[0], _start[1])
            end_pos = (_end[0] - _start[0], _end[1] - _start[1])
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = start_pos
            shape = pymunk.Segment(body, (0, 0), end_pos, 0.1)
            shape.elasticity = 1
            shape.collision_type = 2 + i
            self.bodies.append(body)
            self.shapes.append(shape)
            self.collision_type_list.append(shape.collision_type)
            if i == 0:
                self.line = Line(start=_start, end=_end, color=BROWN, **kwargs)
                self.line.set_opacity(0)
                self.land = Polygon(
                    (-1 * config.frame_width / 2, self.line.get_y(), 0),
                    (1 * config.frame_width / 2, self.line.get_y(), 0),
                    (1 * config.frame_width / 2, -config.frame_height / 2, 0),
                    (-1 * config.frame_width / 2, -config.frame_height / 2, 0),
                )
                self.land.set_fill(BROWN, opacity=1)
                self.land.set_stroke(opacity=0)

    def max_collision_type(self):
        return max(self.collision_type_list)

# ground = Ground(y_pos=-3, start=LEFT * 10, end=RIGHT * 10, color=GREY)