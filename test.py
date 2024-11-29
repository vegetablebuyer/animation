from manim import *

from physic.man.man import Man
from physic.ground import PhysicalGround
from physic.space import PhysicalSpace

class TestMan(MovingCameraScene):
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



        body = main_role.it()
        self.play(FadeIn(body))

        main_role.turn_right()
        self.wait(2)
        main_role.turn_left()
        self.wait(2)

        main_role.walk_left()
        self.wait(5)

        main_role.stop_walk_left()
        self.wait(2)

class DrawLineToCircleEdge(Scene):
    def construct(self):
        # Step 1: 创建一个圆形
        radius = 2
        circle = Circle(radius=radius, color=BLUE)
        self.add(circle)

        # Step 2: 选择圆内的一个随机起始点
        # 这里我们选择一个相对于圆心的固定点来做示例
        start_point = circle.get_center() + DOWN * 1  # 在圆内的一个点

        # Step 3: 计算从起始点到圆边界的交点
        # 方向向量是从圆心到起始点的方向
        x0, y0, z0 = start_point
        end_x = np.sqrt(radius ** 2 - y0 ** 2)  # 通过圆方程计算在 y0 高度下的边界点的 x 坐标
        end_point = np.array([end_x, y0, 0])
        # Step 4: 创建一条从起点到圆边缘的直线
        line = Line(start=start_point, end=end_point, color=RED)

        # 将起点和直线添加到场景中
        dot = Dot(start_point, color=YELLOW)  # 标记起始点
        self.add(dot, line)

        # 停留一段时间以便观察效果
        self.wait(2)