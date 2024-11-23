from manim import *
from manim.typing import Point3D
import pymunk


class PhysicalLine(Line):
    def __init__(self, start: Point3D, end: Point3D, **kwargs):
        super().__init__(start=start, end=end, **kwargs)

        start_pos = (start[0], start[1])
        end_pos = (end[0] - start[0], end[1] - start[1])
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        # self.body = pymunk.Body(1, pymunk.moment_for_segment(1, (0, 0), end_pos, 0.1))
        self.body.position = start_pos
        self.shape = pymunk.Segment(self.body, (0, 0), end_pos, 0.1)
        self.shape.collision_type = 2
        self.add_updater(self.align_position)

    def align_position(self, obj, dt):
        start = self.get_start()
        start_pos = (start[0], start[1])
        self.body.position = start_pos


class PhysicalCircle(Circle):
    def __init__(self, radius: float = None, color: ParsableManimColor = RED,
                 elasticity=0.8, density=1, pos=(0, 0), **kwargs):
        super().__init__(radius=radius, color=color, **kwargs)
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = self.get_center()[0] + pos[0], self.get_center()[1] + pos[1]
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = elasticity
        self.shape.density = density
        self.shape.collision_type = 2
        self.add_updater(self.align_position)

    def align_position(self, obj, dt):
        start = self.get_center()
        start_pos = (start[0], start[1])
        self.body.position = start_pos


class PhysicalRoundedRectangle(RoundedRectangle):
    def __init__(self, width: float=1, height: float=1, **kwargs):
        super().__init__(width=width, height=height, **kwargs)
        position = self.get_center()
        moment = pymunk.moment_for_box(1, (width, height))
        self.body = pymunk.Body(1, moment)
        self.body.position = position[0], position[1]

        points = [
            (-width / 2, -height / 2),
            (width / 2, -height / 2),
            (width / 2, height / 2),
            (-width / 2, height / 2),
        ]

        self.shape = pymunk.Poly(self.body, points)
        self.shape.density = 1
        self.shape.elasticity = 0.5
        self.shape.collision_type = 2
        self.add_updater(self.align_position)

    def align_position(self, obj, dt):
        position = self.get_center()
        start_pos = (position[0], position[1])
        self.body.position = start_pos


