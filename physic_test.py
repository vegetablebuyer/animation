import random
from manim import *
import pymunk


class Space(Mobject):
    def __init__(self, dt, gravity=-9.8, **kwargs):
        Mobject.__init__(self, **kwargs)
        self.space = pymunk.Space()
        self.space.gravity = 0, gravity
        self.dt = dt
        self.add_updater(step)

    def add_body(self, *bodys):
        for body in bodys:
            if body.body != self.space.static_body:
                self.space.add(body.body)
            self.space.add(body.shape)

def step(space, dt):
    space.space.step(dt)

def simulate(b):
    x, y = b.body.position
    b.move_to(x * RIGHT + y * UP)
    b.rotate(b.body.angle - b.angle)
    b.angle = b.body.angle

class PhyCircle(Circle):
    def __init__(self, radius: float = None, c_color: ParsableManimColor = RED,
                 velocity=(0, 0), elasticity=0.8, density=1, pos=(0, 0), **kwargs):
        super().__init__(radius=radius, color=c_color, **kwargs)
        self.body = pymunk.Body()
        self.body.velocity = velocity
        self.body.position = self.get_center()[0] + pos[0], self.get_center()[1] + pos[1]
        self.shape = pymunk.Circle(self.body, self.get_width() / 2)
        self.shape.elasticity = elasticity
        self.shape.density = density
        self.angle = 0
        self.add_updater(simulate)

class WallVertical(Rectangle):
    def __init__(self, width=0.1, height=20, position_x=0, **kwargs):
        super().__init__(width=width, height=height, **kwargs)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (position_x, -5), (position_x, 5), 0.1)
        self.shift(position_x * RIGHT)
        self.shape.elasticity = 0.99

class WallHorizontal(Rectangle):
    def __init__(self, width=20, height=0.1, position_y=0, **kwargs):
        super().__init__(width=width, height=height, **kwargs)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (-10, position_y), (10, position_y), 0.1)
        self.shift(position_y * UP)
        self.shape.elasticity = 0.99

class TestPhyCircle(Scene):
    def construct(self):
        num = NumberPlane()
        space = Space(1 / self.camera.frame_rate)
        self.add(space)
        wall = WallVertical(position_x=-5).set_fill(BLUE, 1)
        wall3 = WallVertical(position_x=5).set_fill(BLUE, 1)
        wall2 = WallHorizontal(position_y=-2).set_fill(BLUE, 1)
        phy_circle = PhyCircle(radius=0.5, pos=(0, 3)).set_fill(RED, 1)
        space.add_body(wall, wall3, wall2)
        self.add(wall, wall3, wall2)
        for _ in range(30):
            self.wait()
            rom1 = 2*random.random()
            rom2 = 2 * random.random()
            phy_circle = PhyCircle(radius=0.5, velocity=(rom1, rom2), pos=(rom1, 4)).set_fill(RED, 1)
            space.add_body(phy_circle)
            self.add(phy_circle)
        self.wait(10)