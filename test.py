from manim import *
from manim.utils.color.XKCD import BROWN


class A(Scene):
    def construct(self):
        # 绘制贯穿屏幕的线
        line = Line(start=LEFT * config.frame_width / 2, end=RIGHT * config.frame_width / 2)
        line.set_y(-1)  # 将线的位置设置为屏幕下方一定高度
        line.set_color(WHITE)

        # 绘制线以下的区域（模拟土地）
        land = Polygon(
            (-1 * config.frame_width / 2, line.get_y(), 0),  # 左下角
            (1 * config.frame_width / 2, line.get_y(), 0),  # 右下角
            (1 * config.frame_width / 2, -config.frame_height / 2, 0),  # 右上角
            (-1 * config.frame_width / 2, -config.frame_height / 2, 0),  # 左上角
        )
        land.set_fill(BROWN, opacity=1)  # 设置土地颜色

        # 添加到场景
        self.add(land, line)


        # 停留以观察最终效果
        self.wait(2)
