from pyglet import shapes
import config


class Decor:
    def __init__(self):
        self.border_left = shapes.Rectangle(x=0, y=0, width=config.BORDER_WIDTH, height=config.WINDOW_HEIGHT, color=config.GREEN)
        self.border_right = shapes.Rectangle(x=config.WINDOW_WIDTH-config.BORDER_WIDTH, y=0, width=config.BORDER_WIDTH, height=config.WINDOW_HEIGHT, color=config.BLUE)
        self.middle_line = shapes.Rectangle(x=config.WINDOW_WIDTH/2-1, y=0, width=2, height=config.WINDOW_HEIGHT, color=config.WHITE)
        self.middle_line.opacity = 100

    def draw(self):
        self.border_left.draw()
        self.border_right.draw()
        self.middle_line.draw()
