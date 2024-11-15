from manim import *
import math

class A(Scene):
    def construct(self):
        # 创建线 A 和圆 B
        line_a = Line(start=LEFT, end=RIGHT * 0.5, color=YELLOW)
        circle_b = Circle(radius=0.3, color=BLUE).shift(RIGHT)

        # 将 A 和 B 组合成一个整体 C
        C = VGroup(line_a, circle_b)

        # 将整体 C 放在初始位置
        C.shift(LEFT * 4)

        # 添加 C 到场景
        self.add(C)

        # 定义 A 的摆动更新函数
        def swing_updater(obj, dt):
            angle = 0.2 * np.sin(x)  # 摆动幅度和频率
            obj.rotate(angle, about_point=obj.get_start())

        # 添加摆动的更新器到 A
        line_a.add_updater(swing_updater)

        # 让 C 整体向右移动
        self.play(C.animate.shift(RIGHT * 6), run_time=4)

        # 停止更新器以结束动画
        line_a.remove_updater(swing_updater)

        # 保持场景
        self.wait(1)
