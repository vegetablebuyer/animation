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
                    # space.scene.remove(obj)
                    return True
                else:
                    print("yyyyy")
                    return True

        def post_solve_collision(arbiter, space, data):
            print("雨滴开始与地面发生碰撞")
            return True  # 继续进行碰撞处理

        def separate_collision(arbiter, space, data):
            print("雨滴与地面分离")
            return True

        handler.begin = begin_collision
        handler.post_solve = begin_collision
        handler.separate = begin_collision

        def add_random_raindrop(dt):
            for _ in range(10):
                # if len(rain_list) >= 10:
                #     return

                rain = RainDrop(color=BLUE)
                self.add(rain.rain)
                space.add_body(rain)
                # rain_list.append(rain.rain)

        self.add_updater(add_random_raindrop)
        self.wait(5)

        self.remove_updater(add_random_raindrop)


        # for _ in range(10):
        #     rain = RainDrop(color=BLUE)
        #     self.add(rain.rain)
        #     space.add_body(rain)
        #     rain_list.append(rain)
        # self.wait(2)
        #
        # for a in rain_list:
        #     a.shape.manim_obj.clear_updaters()
        #     space.space.scene.remove(a.shape.manim_obj)
        #     self.wait(0.5)
        # self.wait(1)


