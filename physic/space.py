from manim import *
import pymunk


def step(obj, dt):
    obj.space.step(dt)


class PhysicalSpace(Mobject):
    def __init__(self, scene, dt, gravity=-2, **kwargs):
        Mobject.__init__(self, **kwargs)

        self.space = pymunk.Space()
        self.space.scene = scene
        self.space.gravity = 1, gravity
        self.dt = dt
        self.add_updater(step)
        self.type_handle_list = []

    def add_body_and_shape(self, *bodies) -> None:
        for body in bodies:
            self.space.add(body.body)
            self.space.add(body.shape)

    def add_body(self, *bodies) -> None:
        for body in bodies:
            self.space.add(body)

    def add_shape(self, *shapes):
        for shape in shapes:
            self.space.add(shape)

    def register_collision_event(self, type_a:int, type_b:int)-> pymunk.collision_handler:
        if (type_a, type_b) in self.type_handle_list:
            return None
        handler = self.space.add_collision_handler(type_a, type_b)
        self.type_handle_list.append((type_a, type_b))
        return handler

