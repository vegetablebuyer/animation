from manim import *

from physic.ground import PhysicalGround
from physic.space import PhysicalSpace
from physic.rain import RainDrop, collision_handle
from physic.man.man import Man


class RainScene(Scene):
    def construct(self):
        space = PhysicalSpace(self, 1 / config.frame_rate)
        self.add(space)
        ground = PhysicalGround(y_pos=-1, start=LEFT * 10, end=RIGHT * 10)
        self.add(ground.line)
        self.add(ground.land)
        space.add_body(*ground.bodies)
        space.add_shape(*ground.shapes)

        default_handler = space.space.add_default_collision_handler()
        default_handler.begin = lambda arbiter, space, data: False

        def add_random_raindrop(dt):
            for i in range(1, len(ground.collision_type_list) + 1):
                for _ in range(5):

                    rain = RainDrop(collision_type=ground.max_collision_type() + i, color=WHITE)
                    self.add(rain.rain)
                    space.add_body_and_shape(rain)
                    handler = space.register_collision_event(rain.shape.collision_type, ground.collision_type_list[i-1])
                    if handler is not None:
                        collision_handle(handler)
        self.add_updater(add_random_raindrop)
        self.wait(5)
        self.remove_updater(add_random_raindrop)
        self.wait(2)


class ManWalkingInRain(MovingCameraScene):
    def construct(self):
        space = PhysicalSpace(self, 1 / config.frame_rate)
        self.add(space)
        ground = PhysicalGround(y_pos=-2, start=LEFT * 10, end=RIGHT * 10)
        self.add(ground.line)
        self.add(ground.land)
        space.add_body(*ground.bodies)
        space.add_shape(*ground.shapes)

        default_handler = space.space.add_default_collision_handler()
        default_handler.begin = lambda arbiter, space, data: False

        main_role = Man(ground.line.get_bottom() -1 , 0.5)
        space.add_body_and_shape(*main_role.bodies)


        def add_random_raindrop(dt):
            for i in range(1, len(ground.collision_type_list) + 1):
                for _ in range(2):

                    rain = RainDrop(collision_type=ground.max_collision_type() + i, color=WHITE)
                    self.add(rain.rain)
                    space.add_body_and_shape(rain)
                    handler = space.register_collision_event(rain.shape.collision_type,
                                                             ground.collision_type_list[i - 1])
                    if handler is not None:
                        collision_handle(handler)

        self.add_updater(add_random_raindrop)
        body = main_role.it()
        self.play(FadeIn(body))

        main_role.walk_left()
        self.wait(5)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to(main_role.head).set(width=main_role.head.width * 4))
        main_role.stop_walk_left()
        main_role.stand_straight()
        self.wait(2)

        main_role.walk_right()
        self.wait(5)
        self.play(Restore(self.camera.frame))
        main_role.stop_walk_right()
        main_role.stand_straight()
        self.wait(2)
        self.remove_updater(add_random_raindrop)

