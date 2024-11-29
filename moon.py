from manim import *


class CrescentMoon(Scene):
    def construct(self):

        full_circle = Circle(radius=0.5, color=YELLOW, fill_opacity=1)

        cutout_circle = Circle(radius=0.5, color=BLACK, fill_opacity=1).move_to(
            full_circle.get_center() + RIGHT * full_circle.radius * 0.5)

        crescent_moon = Difference(full_circle, cutout_circle, fill_opacity=0.5).set_color(LIGHTER_GRAY).move_to(
            ORIGIN + config.frame_width/2 * LEFT + UP * 2 )

        self.add(crescent_moon)
        def leaning_updater(mobject, dt):

            lean_strength = 0.05
            for point in mobject.get_points():
                x, y, z = point
                point[1] = y + lean_strength * x

        self.play(crescent_moon.animate.move_to(ORIGIN[0] + crescent_moon.get_center()*UP), run_time=1)
        crescent_moon.add_updater(leaning_updater)
        self.wait(0.5)

        crescent_moon.remove_updater(leaning_updater)

        self.wait(2)


