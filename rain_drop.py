from unittest.mock import right

from manim import *
import pymunk
import random

class RainDropletsWithCollision(Scene):
    def construct(self):
        # 创建地面
        ground_line = Line(start=LEFT * 10, end=RIGHT * 10, color=GREY).shift(DOWN * 3)
        self.add(ground_line)

        # Pymunk 物理世界
        space = pymunk.Space()
        space.gravity = (3, -10)  # 设置重力方向和大小

        # 地面对象
        ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        ground_shape = pymunk.Segment(ground_body, (-6, -3), (6, -3), 0.1)
        ground_shape.elasticity = 0.9
        space.add(ground_body, ground_shape)

        # 容器存储雨滴对象
        droplets = []

        # 创建雨滴
        def create_raindrop():
            x_position = random.uniform(-10, 10)  # 雨滴随机水平位置
            start_pos = (x_position, 3)  # 雨滴初始位置
            end_pos = (x_position + 0.2, 2.7)  # 雨滴的另一端

            # Pymunk 物理长条
            droplet_body = pymunk.Body(1, pymunk.moment_for_segment(1, start_pos, end_pos, 0.05))
            droplet_body.position = start_pos
            droplet_shape = pymunk.Segment(droplet_body, (0, 0), (0, -0.5), 0.05)  # 雨滴形状
            droplet_shape.elasticity = 0.6
            droplet_shape.collision_type = 1  # 设置碰撞类型

            space.add(droplet_body, droplet_shape)

            # Manim 的雨滴表示为一条线
            droplet_mobject = Line(
                start=(x_position, 3, 0),
                end=(x_position + 0.2, 2.7, 0),
                color=BLUE,
                stroke_width=3
            )
            droplets.append((droplet_body, droplet_mobject))
            self.add(droplet_mobject)

        # 碰撞回调函数
        def on_collision(arbiter, space, data):
            # 获取雨滴的位置
            body = arbiter.shapes[0].body
            pos = body.position

            # 模拟水花效果（用小圆点表示）
            for _ in range(3):
                splash = Dot(point=[pos.x + random.uniform(-0.2, 0.2), pos.y + random.uniform(0.1, 0.3), 0], radius=0.05, color=WHITE)
                self.add(splash)
                self.remove(splash)

            return True  # 继续处理其他碰撞事件

        # 注册碰撞处理器
        handler = space.add_collision_handler(1, 0)  # 1 为雨滴，0 为地面
        handler.post_solve = on_collision

        # 更新雨滴位置
        def update_droplets(dt):
            space.step(dt)  # 更新物理引擎
            for body, mobject in droplets:
                pos = body.position
                angle = body.angle
                mobject.put_start_and_end_on(
                    [pos.x, pos.y, 0],
                    [pos.x + 0.2 + 0.3 * np.sin(angle), pos.y - 0.3 * np.cos(angle), 0]
                )

                # 如果雨滴越过地面以下，则重新生成
                if pos.y < -3.5:
                    body.position = (random.uniform(-10, 10), 3)
                    body.velocity = (0, 0)

        # 动态添加雨滴
        def add_rain(dt):
            for _ in range(5):  # 每帧添加 5 个雨滴
                create_raindrop()

        # 添加更新器
        self.add_updater(update_droplets)
        self.add_updater(add_rain)

        # 动画运行一段时间
        self.wait(5)

        # 停止更新器
        self.remove_updater(update_droplets)
        self.remove_updater(add_rain)

class A(Scene):
    def construct(self):
        x_position = random.uniform(-6, 6)
        droplet_mobject = Line(
            start=(x_position, 3, 0),
            end=(x_position + 0.2, 3.3, 0),
            color=PINK,
            stroke_width=3
        )
        self.add(droplet_mobject)
        self.wait(3)