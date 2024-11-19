from manim import *
from manim.typing import Point3D
import pymunk
import random


class Space(Mobject):
    def __init__(self, dt, gravity=-3, **kwargs):
        Mobject.__init__(self, **kwargs)
        self.space = pymunk.Space()
        self.space.gravity = 0, gravity
        self.dt = dt
        self.add_updater(step)

    def add_body(self, *bodies):
        for body in bodies:
            self.space.add(body.body)
            self.space.add(body.shape)


def step(obj, dt):
    obj.space.step(dt)


def update_raindrop(obj, dt):
    body = obj.body
    pos = body.position
    obj.put_start_and_end_on(
        [pos.x, pos.y, 0],
        [pos.x, pos.y - 0.3, 0]
    )
    obj.angle = obj.body.angle

    if pos.y < -3.5:
        body.position = (random.uniform(-10, 10), 5)
        body.velocity = (0, 0)


def update_circle(obj, dt):
    x, y = obj.body.position
    # print("cricle:", obj.body.position.y)
    obj.move_to(x * RIGHT + y * UP)
    obj.rotate(obj.body.angle - obj.angle)
    obj.angle = obj.body.angle


class RainDrop(Line):
    def __init__(self, **kwargs):
        x_pos = random.uniform(-6, 6)
        # x_pos = 0
        y_pos = 3
        start_pos = (0, 0)  # 雨滴初始位置
        end_pos = (0, -0.3)  # 雨滴的另一端
        super().__init__(start=(x_pos, y_pos, 0), end=(x_pos, y_pos - 0.3, 0), **kwargs)
        # self.body = pymunk.Body()
        self.body = pymunk.Body(1, pymunk.moment_for_segment(1, start_pos, end_pos, 0.05))
        self.body.position = x_pos, y_pos
        self.shape = pymunk.Segment(self.body, start_pos, end_pos, 0.05)
        self.shape.elasticity = 0.5
        self.shape.density = 1
        self.add_updater(update_raindrop)


class PhyCircle(Circle):
    def __init__(self, radius: float = None, c_color: ParsableManimColor = RED,
                 elasticity=0.8, density=1, pos=(-3, 6), **kwargs):
        super().__init__(radius=radius, color=c_color, **kwargs)
        self.body = pymunk.Body()
        # self.body.velocity = velocity
        self.body.position = self.get_center()[0] + pos[0], self.get_center()[1] + pos[1]
        self.shape = pymunk.Circle(self.body, self.get_width() / 2)
        self.shape.elasticity = elasticity
        self.shape.density = density
        self.angle = 0
        self.add_updater(update_circle)


class Ground(Line):
    def __init__(self, g_y_pos: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)

        self.shape = pymunk.Segment(self.body, (-10, g_y_pos), (10, g_y_pos), 0.1)
        self.shape.elasticity = 1
        # self.shape.collision_type = 2
        self.shift(g_y_pos * UP)


class RainScene(Scene):
    def construct(self):
        space = Space(1 / config.frame_rate)
        self.add(space)

        ground = Ground(g_y_pos=-3, start=LEFT * 10, end=RIGHT * 10, color=GREY)
        self.add(ground)

        space.add_body(ground)

        def add_random_raindrop(dt):
            for _ in range(10):
                # if len(rain_list) >= 20:
                #     return
                rain = RainDrop(color=BLUE)
                self.add(rain)
                space.add_body(rain)
                # rain_list.append(rain)

        self.add_updater(add_random_raindrop)
        self.wait(5)
        self.remove_updater(add_random_raindrop)


class CircleScene(Scene):
    def construct(self):
        print(config.frame_height)
        space = Space(1 / config.frame_rate)
        self.add(space)

        x = Ground(g_y_pos=3, start=LEFT * 10, end=RIGHT * 10, color=PINK)
        self.add(x)

        space.add_body(x)

        z = list()

        def add_random_circle(dt):
            for _ in range(1):
                if len(z) >= 1:
                    return
                c = PhyCircle(radius=0.5).set_fill(GREEN, True)
                self.add(c)
                space.add_body(c)
                z.append(c)

        self.add_updater(add_random_circle)
        self.wait(10)
        self.remove_updater(add_random_circle)
