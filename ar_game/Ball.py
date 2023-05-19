import time
import random
from pyglet import shapes
import config


class Ball:
    def __init__(self):
        self.x = self.y = 0
        self.vx = self.vy = 0
        self.min_v = config.INIT_BALL_V_EASY[0]
        self.max_v = config.INIT_BALL_V_EASY[1]
        self.body = shapes.Circle(x=config.WINDOW_WIDTH / 2, y=config.WINDOW_HEIGHT / 2, radius=config.WINDOW_WIDTH / 50, color=config.HEIDENELKE)
        self.init()

    def init(self):
        self.body.x = config.WINDOW_WIDTH / 2
        self.body.y = config.WINDOW_HEIGHT / 2
        rx = random.randint(self.min_v, self.max_v)
        ry = random.randint(self.min_v, self.max_v)
        self.vx = rx if bool(random.getrandbits(1)) else -rx
        self.vy = ry if bool(random.getrandbits(1)) else -ry

    def reset_on_goal(self):
        self.min_v += 1
        self.max_v += 1
        self.init()

    def reset_on_over(self):
        self.min_v = config.INIT_BALL_V_EASY[0]
        self.max_v = config.INIT_BALL_V_EASY[1]
        self.init()

    def hit_test(self, thresh):
        try:
            current_color = thresh[int(config.WINDOW_HEIGHT - self.body.y)][int(self.body.x)]
            if current_color[1] != config.WHITE_SINGLE:
                self.vx = -self.vx
                self.vy = -self.vy
        except:
            return

    def update(self):
        if self.body.y - self.body.radius <= 0 or self.body.y + self.body.radius >= config.WINDOW_HEIGHT:
            self.vy = -self.vy
        self.body.x += self.vx
        self.body.y += self.vy

    def draw(self):
        self.body.draw()
