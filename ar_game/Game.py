import cv2
import config
from Ball import Ball
from Decor import Decor
from pyglet import text


class Game:
    def __init__(self, window_height):
        self.window_height = window_height
        self.width = self.height = self.x = self.y = 0
        self.running_countdown = self.score_a = self.score_b = 0

        self.score_a_label = text.Label("Player A: 0", x=config.BORDER_WIDTH + 10, y=config.WINDOW_HEIGHT - 20, anchor_x='left', anchor_y='center', color=config.BLACK)
        self.score_b_label = text.Label("Player B: 0", x=config.WINDOW_WIDTH - config.BORDER_WIDTH - 10, y=config.WINDOW_HEIGHT - 20, anchor_x='right', anchor_y='center', color=config.BLACK)
        self.player_a_score_text = "Player A scored!"
        self.player_b_score_text = "Player B scored!"
        self.player_a_win_text = "Player A won!"
        self.player_b_win_text = "Player B won!"
        self.scored_label = text.Label(self.player_a_score_text, x=config.WINDOW_WIDTH / 2, y=config.WINDOW_HEIGHT / 1.6, anchor_x='center', anchor_y='center', color=config.HEIDENELKE, font_size=config.FONT_SIZE_BIG)
        self.countdown_label = text.Label("Get ready...", x=config.WINDOW_WIDTH / 2, y=config.WINDOW_HEIGHT/2, anchor_x='center', anchor_y='center', color=config.HEIDENELKE, font_size=config.FONT_SIZE_BIG)
        self.over_winner_label = text.Label(self.player_a_score_text, x=config.WINDOW_WIDTH / 2, y=config.WINDOW_HEIGHT / 1.6, anchor_x='center', anchor_y='center', color=config.HEIDENELKE, font_size=config.FONT_SIZE_BIG)
        self.over_restart_label = text.Label("Press SPACE to restart", x=config.WINDOW_WIDTH / 2, y=config.WINDOW_HEIGHT / 2, anchor_x='center', anchor_y='center', color=config.HEIDENELKE, font_size=config.FONT_SIZE_BIG)

        self.ball = Ball()
        self.decor = Decor()
        self.game_state = 2

    def restart(self):
        self.ball.reset_on_over()
        self.running_countdown = 0
        self.score_a = 0
        self.score_b = 0
        self.score_a_label.text = f"Player A: {self.score_a}"
        self.score_b_label.text = f"Player B: {self.score_b}"
        self.game_state = 0

    def goal_test(self):
        """
        check and handle ball's collision with goals:
        increase scores, reset ball and set game state to 'get ready again'
        """
        if self.ball.body.x + self.ball.body.radius <= config.BORDER_WIDTH:
            self.score_b += 1
            self.score_b_label.text = f"Player B: {self.score_b}"
            self.scored_label.text = self.player_b_score_text
            self.ball.reset_on_goal()
            self.game_state = -1
        elif self.ball.body.x - self.ball.body.radius >= config.WINDOW_WIDTH - config.BORDER_WIDTH:
            self.score_a += 1
            self.score_a_label.text = f"Player A: {self.score_a}"
            self.scored_label.text = self.player_a_score_text
            self.ball.reset_on_goal()
            self.game_state = -1

    def over_test(self):
        """
        check if one of the players has reached score to win
        if so, set game state to 'game finished'
        """
        if self.score_b >= config.SCORE_WIN:
            self.over_winner_label.text = self.player_b_win_text
            self.game_state = 1
        elif self.score_a >= config.SCORE_WIN:
            self.over_winner_label.text = self.player_a_win_text
            self.game_state = 1

    def update(self, img):
        """
        if game running, calc binary threshold img of current webcam capture
        based on this, check if a player scored, the game has finished and update ball
        """
        if self.game_state == 0:
            ret, thresh = cv2.threshold(img, config.THRESHOLD, config.WHITE_SINGLE, cv2.THRESH_BINARY)
            self.goal_test()
            self.over_test()
            self.ball.hit_test(thresh)
            self.ball.update()

    def draw_get_ready(self):
        """
        draw label 'get ready' and
        wait <WAIT_AFTER_GOAL> ticks to continue game
        """
        self.countdown_label.draw()
        self.running_countdown += 1
        if self.running_countdown >= config.WAIT_AFTER_GOAL:
            self.game_state = 0
            self.running_countdown = 0

    def draw(self):
        # game running
        if self.game_state == 0:
            self.ball.draw()
        # game finished
        elif self.game_state == 1:
            self.over_winner_label.draw()
            self.over_restart_label.draw()
        # game paused because a player scored
        elif self.game_state == -1:
            self.scored_label.draw()
            self.draw_get_ready()
        # initial state
        # in the beginning, you have <WAIT_AFTER_GOAL> ticks to get game board ready
        elif self.game_state == 2:
            self.draw_get_ready()

        self.decor.draw()
        self.score_a_label.draw()
        self.score_b_label.draw()


