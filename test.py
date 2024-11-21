from manim import *
from manim.typing import Point3D
import pymunk
import random


class Space(Mobject):
    def __init__(self, scene, dt, gravity=-2, **kwargs):
        Mobject.__init__(self, **kwargs)

        self.space = pymunk.Space()
        self.space.scene = scene
        self.space.gravity = 1, gravity
        self.dt = dt
        self.add_updater(step)

    def add_body(self, *bodies):
        for body in bodies:
            self.space.add(body.body)
            self.space.add(body.shape)


def step(obj, dt):
    obj.space.step(dt)


def simulate(obj, dt, body):
    body.position = obj.get_center()[0] - 0.05, obj.get_center()[1]
    obj.move_to((obj.get_center()[0] - 0.05) * RIGHT + obj.get_center()[1] * UP)


def update_raindrop(obj, dt, body):
    pos = body.position
    obj.put_start_and_end_on(
        [pos.x, pos.y, 0],
        [pos.x - 0.2, pos.y + 0.3, 0]
    )


class RainDrop(object):
    def __init__(self, **kwargs):
        x_pos = random.uniform(-10, 10)
        y_pos = 6
        start_pos = (0, 0)  # 雨滴初始位置
        end_pos = (-0.2, 0.3)  # 雨滴的另一端
        self.rain = Line(start=(x_pos, y_pos, 0), end=(x_pos - 0.2, y_pos + 0.3, 0), **kwargs)
        # self.body = pymunk.Body()
        self.body = pymunk.Body(1, pymunk.moment_for_segment(1, start_pos, end_pos, 0.05))
        self.body.position = x_pos, y_pos
        self.shape = pymunk.Segment(self.body, start_pos, end_pos, 0.05)
        self.shape.elasticity = 0.5
        self.shape.density = 1
        self.shape.collision_type = 1
        self.rain.add_updater(lambda mob, dt: update_raindrop(mob, dt, body=self.body))
        self.shape.manim_obj = self.rain


class PhyCircle(object):
    def __init__(self, radius: float = None, c_color: ParsableManimColor = RED,
                 velocity=(0, 0), elasticity=0.8, density=1, pos=(0, 0), **kwargs):
        self.circle = Circle(radius=radius, color=c_color, **kwargs).set_fill(RED, 1)
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.velocity = velocity
        self.body.position = self.circle.get_center()[0] + pos[0], self.circle.get_center()[1] + pos[1]
        self.shape = pymunk.Circle(self.body, self.circle.get_width() / 2)
        self.shape.elasticity = elasticity
        self.shape.density = density
        self.shape.collision_type = 2
        self.circle.add_updater(lambda mob, dt: simulate(mob, dt, body=self.body))


class Ground(Line):
    def __init__(self, g_y_pos: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)

        self.shape = pymunk.Segment(self.body, (-10, g_y_pos), (10, g_y_pos), 0.1)
        self.shape.elasticity = 1
        self.shape.collision_type = 2
        self.shift(g_y_pos * UP)


class RainScene(Scene):
    def construct(self):
        space = Space(self, 1 / config.frame_rate)
        self.add(space)
        ground = Ground(g_y_pos=-3, start=LEFT * 10, end=RIGHT * 10, color=GREY)
        self.add(ground)

        space.add_body(ground)
        handler = space.space.add_collision_handler(1, 2)

        a = PhyCircle(radius=1, pos=(0, 0))
        space.add_body(a)
        self.add(a.circle)

        def begin_collision(arbiter, space, data):
            shape_a, shape_b = arbiter.shapes
            for shape in [shape_a, shape_b]:
                if hasattr(shape, "manim_obj"):
                    obj = shape.manim_obj
                    obj.put_start_and_end_on(
                            [0, 0, 0],
                            [0, 0, 0]
                    )
                    space.remove(shape, shape.body)
                    obj.clear_updaters()
                    space.scene.remove(obj)
                    return True
                else:
                    return True

        def post_solve_collision(arbiter, space, data):
            return True  # 继续进行碰撞处理

        def separate_collision(arbiter, space, data):
            return True

        handler.begin = post_solve_collision
        handler.post_solve = begin_collision
        handler.separate = post_solve_collision

        def add_random_raindrop(dt):
            for _ in range(20):

                rain = RainDrop(color=BLUE)
                self.add(rain.rain)
                space.add_body(rain)

        self.add_updater(add_random_raindrop)
        self.wait(10)

        self.remove_updater(add_random_raindrop)
        self.wait(5)
        print("end number", len(self.mobjects))

