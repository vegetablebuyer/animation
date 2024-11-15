from manim import *

class B(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        self.add(axes)

        self.begin_ambient_camera_rotation(rate=-0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()