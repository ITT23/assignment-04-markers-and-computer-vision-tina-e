import cv2
import pyglet
from PIL import Image
import sys
from MarkerDetection import MarkerDetector
from Game import Game
import config

video_id = 0

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])
    if sys.argv[2]:
        try:
            config.SCORE_WIN = int(sys.argv[2])
        except:
            print("WARN: No valid input for: Score to Win\nDefault value set.")
    if sys.argv[3]:
        if sys.argv[3].lower() == 'easy':
            config.INIT_BALL_V = config.INIT_BALL_V_EASY
        elif sys.argv[3].lower() == 'medium':
            config.INIT_BALL_V = config.INIT_BALL_V_MEDIUM
        elif sys.argv[3].lower() == 'hard':
            config.INIT_BALL_V = config.INIT_BALL_V_HARD
        else:
            print("WARN: No valid input for: Difficulty\nDefault value set.")


# converts OpenCV image to PIL image and then to pyglet texture
# https://gist.github.com/nkymut/1cb40ea6ae4de0cf9ded7332f1ca0d55
def cv2glet(img, fmt):
    """Assumes image is in BGR color space. Returns a pyimg object"""
    if fmt == 'GRAY':
      rows, cols = img.shape
      channels = 1
    else:
      rows, cols, channels = img.shape

    raw_img = Image.fromarray(img).tobytes()

    top_to_bottom_flag = -1
    bytes_per_row = channels*cols
    pyimg = pyglet.image.ImageData(width=cols, 
                                   height=rows, 
                                   fmt=fmt, 
                                   data=raw_img, 
                                   pitch=top_to_bottom_flag*bytes_per_row)
    return pyimg


# Create a video capture object for the webcam
cap = cv2.VideoCapture(video_id)
print(cap)

window = pyglet.window.Window(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
aruco_detector = MarkerDetector(cap.read())
game = Game(config.WINDOW_HEIGHT)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        game.restart()
    elif symbol == pyglet.window.key.Q:
        sys.exit(0)


@window.event
def on_draw():
    window.clear()
    ret, frame = cap.read()
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_detector.detect(img_gray)
    has_found_board = aruco_detector.warp(frame)
    if has_found_board:
        game.update(aruco_detector.out_img)
    img = cv2glet(aruco_detector.out_img, 'BGR')
    img.blit(0, 0, 0)
    game.draw()


pyglet.app.run()
