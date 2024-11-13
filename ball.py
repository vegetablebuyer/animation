
from manim import *
import numpy as np


class BouncingBall(Scene):

    def construct(self):
        self.camera.background_color = BLACK
        self.camera.frame_rate = 120

        ball = Circle(radius=0.2, color=PINK, fill_opacity=1)
        ball.stretched = False
        ball.touched_down = False
        ball.move_to(LEFT * 6)
        start = -6
        end = 6

        ground_line = Line(start=LEFT * 7, end=RIGHT * 7, color=GREY)
        ground_y = -3
        ground_line.shift(DOWN * 3)

        A = 2
        k = 0.2
        x_tracker = ValueTracker(start)

        points = [[x, A * abs(np.sin(x)) * np.exp(-k * x) + ground_y, 0] for x in np.linspace(start, end, 100)]
        ball_path = VMobject()
        ball_path.set_points_smoothly(points)

        def update_ball(mob):

            x = x_tracker.get_value()
            y = A * abs(np.sin(x)) * np.exp(-k * x) + ground_y
            if y - mob.radius < ground_y:
                y = ground_y + mob.radius
            mob.move_to(np.array([x, y, 0]))

            if y == (ground_y + mob.radius) and not mob.stretched:
                mob.stretch(0.8, 1)
                mob.stretched = True
                mob.touched_down = True
            else:
                if mob.touched_down:
                    mob.stretch(1.5, 1)
                    mob.touched_down = False
                elif mob.stretched:
                    mob.stretch(5/6, 1)
                    mob.stretched = False

        def update_path(mob):
            length = end - start
            x = x_tracker.get_value()
            point_start = int(((x - start)/length) * len(points))
            if point_start == len(points):
                point_start = len(points) -1
            mob.set_points_smoothly(points[point_start:])

        self.add(ground_line, ball, ball_path)

        ball.add_updater(update_ball)
        ball_path.add_updater(update_path)

        self.play(x_tracker.animate.set_value(end), run_time=5, rate_func=linear)

        ball.remove_updater(update_ball)
        ball_path.remove_updater(update_path)