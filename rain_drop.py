
from manim import *
from manim.typing import Point3D
import pymunk
import random


class Space(Mobject):
    def __init__(self, dt, gravity=-9.8, **kwargs):
        Mobject.__init__(self, **kwargs)
        self.space = pymunk.Space()
        self.space.gravity = 3, gravity
        self.dt = dt
        self.add_updater(step)

    def add_body(self, *bodies):
        for body in bodies:
            if body.body != self.space.static_body:
                self.space.add(body.body)
            self.space.add(body.shape)

def step(obj, dt):
    obj.space.step(dt)

def update_raindrop(obj, dt):
    body = obj.body
    pos = body.position
    obj.put_start_and_end_on(
        [pos.x, pos.y, 0],
        [pos.x + 0.2, pos.y - 0.3, 0]
    )

    if pos.y < -3.5:
        body.position = (random.uniform(-10, 10), 3)
        body.velocity = (0, 0)


class RainDrop(Line):
    def __init__(self, **kwargs):
        x_pos = random.uniform(-10, 10)  # 雨滴随机水平位置
        start_pos = (x_pos, 3)  # 雨滴初始位置
        end_pos = (x_pos + 0.2, 2.7)  # 雨滴的另一端
        super().__init__(start=(x_pos, 3, 0), end=(x_pos + 0.2, 2.7, 0), **kwargs)

        self.body = pymunk.Body(1, pymunk.moment_for_segment(1, start_pos, end_pos, 0.05))
        self.shape = pymunk.Segment(self.body, start_pos, end_pos, 0.05)
        self.shape.elasticity = 0.6
        self.collision_type = 1
        self.add_updater(update_raindrop)


class Ground(Line):
    def __init__(self, y_pos: Point3D, **kwargs):
        super().__init__(**kwargs)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (-6, -3), (6, -3), 0.1)
        self.shape.elasticity = 0.9
        self.shift(y_pos)


class RainScene(Scene):
    def construct(self):

        ground = Ground(y_pos=DOWN * 3, start=LEFT * 10, end=RIGHT * 10, color=GREY)
        self.add(ground)

        space = Space(1/config.frame_rate)

        space.add_body(ground)
        self.add(space)

        def add_random_raindrop(dt):
            for _ in range(5):
                rain = RainDrop(color=BLUE)
                self.add(rain)
                space.add_body(rain)
        self.add_updater(add_random_raindrop)

        self.wait(5)
        self.remove_updater(add_random_raindrop)
