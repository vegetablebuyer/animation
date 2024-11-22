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

    def phy_put_start_and_end_on(self, start: Point3D, end: Point3D):
        self.put_start_and_end_on(start, end)
        start_pos = (start[0], start[1])
        self.body.position = start_pos


class PhysicalCircle(Circle):
    def __init__(self, radius: float = None, c_color: ParsableManimColor = RED,
                 elasticity=0.8, density=1, pos=(0, 0), **kwargs):
        super().__init__(radius=radius, color=c_color, **kwargs)
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = self.get_center()[0] + pos[0], self.get_center()[1] + pos[1]
        self.shape = pymunk.Circle(self.body, self.get_width() / 2)
        self.shape.elasticity = elasticity
        self.shape.density = density
        self.shape.collision_type = 2


class PhysicalRoundedRectangle(RoundedRectangle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = self.get_center()[0] + pos[0], self.get_center()[1] + pos[1]
        self.shape = pymunk.(self.body, self.get_width() / 2)
        self.shape.elasticity = elasticity
        self.shape.density = density
        self.shape.collision_type = 2


