from manim import *
import pymunk
import random


def update_raindrop(obj, dt, body):
    pos = body.position
    obj.put_start_and_end_on(
        [pos.x, pos.y, 0],
        [pos.x - 0.2, pos.y + 0.3, 0]
    )


def update_split_raindrop(obj, dt, shape, space):
    obj.clear_updaters()
    obj.put_start_and_end_on(
        [0, 0, 0],
        [0, 0, 0]
    )
    space.scene.remove(obj)
    space.remove(shape, shape.body)


def begin_collision(arbiter, space, data):
    shape = arbiter.shapes[0]
    collision_point = arbiter.contact_point_set.points[0].point_a
    x, y = collision_point
    # print(shape.collision_type, collision_point)
    left_raindrop = LeftSplitDrop(x - 0.01, y + 0.01, space)
    space.add(left_raindrop.body, left_raindrop.shape)

    right_raindrop = RightSplitDrop(x + 0.01, y + 0.01, space)
    space.add(right_raindrop.body, right_raindrop.shape)

    space.scene.add(left_raindrop.raindrop, right_raindrop.raindrop)

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
    return True


def separate_collision(arbiter, space, data):
    return True


def collision_handle(handler:pymunk.collision_handler):
    handler.begin = begin_collision
    handler.post_solve = post_solve_collision
    handler.separate = separate_collision


class RainDrop(object):
    def __init__(self, collision_type:int = 1, **kwargs):
        x_pos = random.uniform(-12, 12)
        y_pos = 6
        start_pos = (0, 0)
        end_pos = (-0.1, 0.15)
        self.rain = Line(start=(x_pos, y_pos, 0), end=(x_pos - 0.1, y_pos + 0.15, 0), **kwargs)
        self.body = pymunk.Body(1, pymunk.moment_for_segment(1, start_pos, end_pos, 0.03))
        self.body.position = x_pos, y_pos
        self.shape = pymunk.Segment(self.body, start_pos, end_pos, 0.03)
        self.shape.elasticity = 0.5
        self.shape.density = 1
        self.shape.collision_type = collision_type
        self.rain.add_updater(lambda mob, dt: update_raindrop(mob, dt, body=self.body))
        self.shape.manim_obj = self.rain


class SplitDrop(object):
    def __init__(self, pos_x: float = 0, pos_y: float = 0, delta_x: float = 0, delta_y: float = 0, space=None):

        self.raindrop = Line(
            start=(pos_x, pos_y, 0),
            end=(pos_x + delta_x, pos_y + delta_y, 0),
            color=WHITE
        )
        self.body = pymunk.Body(0.1, pymunk.moment_for_segment(0.1, (0, 0), (delta_x, delta_y), 0.03))
        self.body.position = (pos_x, pos_y)
        self.shape = pymunk.Segment(self.body, (0, 0), (delta_x, delta_y), 0.03)
        self.shape.collision_type = 3

        self.raindrop.add_updater(lambda mob, dt: update_split_raindrop(mob, dt, shape=self.shape, space=space))


class LeftSplitDrop(SplitDrop):
    def __init__(self, pos_x: float = 0, pos_y: float = 0, space=None):
        super().__init__(pos_x=pos_x, pos_y=pos_y, delta_x=-0.08, delta_y=0.08, space=space)


class RightSplitDrop(SplitDrop):
    def __init__(self, pos_x: float = 0, pos_y: float = 0, space=None):
        super().__init__(pos_x=pos_x, pos_y=pos_y, delta_x=0.08, delta_y=0.08, space=space)


