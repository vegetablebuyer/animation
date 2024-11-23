
from physic.physic_mobject import *

class Limb(PhysicalLine):

    def __init__(self, start: Point3D, end: Point3D, is_left: bool, **kwargs):
        super().__init__(start=start, end=end, **kwargs)
        self.start_angle = np.arctan2(end[1] - start[1], end[0] - start[0])
        # if -np.pi/2 <= self.start_angle <= np.pi/2:
        if self.start_angle >= 0:
            self.end_angle = np.pi - self.start_angle
        else:
            self.end_angle = -(np.pi - abs(self.start_angle))

        self.is_left = is_left
        if self.is_left:
            self.add = False
        else:
            self.add = True

    def wave(self, obj, dt):
        step = np.pi / 40
        start = obj.get_start()
        end = obj.get_end()
        angle = np.arctan2(end[1] - start[1], end[0] - start[0])
        if 0 <= self.start_angle < np.pi / 2 or -np.pi <= self.start_angle < -np.pi / 2:
            # first quadrant and third quadrant
            if angle <= self.start_angle:
                self.add = True
                obj.rotate(step, about_point=obj.get_start())
                return
            elif angle >= self.end_angle:
                self.add = False
                obj.rotate(-step, about_point=obj.get_start())
                return
        elif np.pi / 2 <= self.start_angle < np.pi or -np.pi / 2 <= self.start_angle < 0:
            # second quadrant and fourth quadrant
            if angle >= self.start_angle:
                self.add = False
                obj.rotate(-step, about_point=obj.get_start())
                return
            elif angle <= self.end_angle:
                self.add = True
                obj.rotate(step, about_point=obj.get_start())
                return

        if self.add:
            obj.rotate(step, about_point=obj.get_start())
        elif not self.add:
            obj.rotate(-step, about_point=obj.get_start())

    def walk(self, obj, dt):
        step = np.pi * dt/3
        start = obj.get_start()
        end = obj.get_end()
        angle = np.arctan2(end[1] - start[1], end[0] - start[0])

        if not (-5/8 * np.pi) <= angle <= (-3/8 * np.pi):
            self.add = not self.add
        if self.add:
            obj.rotate(step, about_point=obj.get_start())
        else:
            obj.rotate(-step, about_point=obj.get_start())

    def start_walk(self):
        self.add_updater(self.walk)

    def stop_walk(self):
        self.remove_updater(self.walk)
        self.set_straight()

    def start_wave(self):
        self.add_updater(self.wave)

    def stop_wave(self):
        self.remove_updater(self.wave)

    def set_straight(self):
        start = self.get_start()
        end = self.get_end()
        angle = np.arctan2(end[1] - start[1], end[0] - start[0])
        if angle < -np.pi /2:
            self.rotate(abs(-np.pi /2 - angle), about_point=self.get_start())
        else:
            self.rotate(-abs(-np.pi /2 - angle), about_point=self.get_start())