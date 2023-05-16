import cv2
import sys
import numpy as np
import math
from imutils import perspective

if len(sys.argv) >= 3:
    print(sys.argv)
    path_in = sys.argv[1]
    path_out = sys.argv[2]
    h_out = int(sys.argv[3]) if sys.argv[3:] else 1920
    w_out = int(sys.argv[4]) if sys.argv[4:] else 1080
    allow_orientation_fix = bool(sys.argv[5]) if sys.argv[5:] else False

else:
    print("ERROR: Please specify input file and output destination")
    sys.exit(1)


WIDTH = w_out
HEIGHT = h_out
ALLOW_ORIENTATION_CHANGE = allow_orientation_fix
DESTINATION_OUT = path_out
WINDOW_NAME = 'Preview Window'
IMG_ORIGINAL = cv2.imread(path_in)

img = IMG_ORIGINAL.copy()
cv2.namedWindow(WINDOW_NAME)

corners = []


def switch_orientation(width, height):
    dx_upper = math.sqrt((corners[0][0] - corners[1][0]) ** 2 + (corners[0][1] - corners[1][1]) ** 2)
    dx_lower = math.sqrt((corners[3][0] - corners[2][0]) ** 2 + (corners[3][1] - corners[2][1]) ** 2)
    dy_left = math.sqrt((corners[0][0] - corners[3][0]) ** 2 + (corners[0][1] - corners[3][1]) ** 2)
    dy_right = math.sqrt((corners[1][0] - corners[2][0]) ** 2 + (corners[1][1] - corners[2][1]) ** 2)

    if (max([dx_upper, dx_lower]) < max([dy_left, dy_right]) and width > height) or (
            max([dx_upper, dx_lower]) > max([dy_left, dy_right]) and width < height):
        return height, width
    return width, height


def transform(width, height, corner_points):
    global IMG_ORIGINAL, corners
    destination = np.uint8(np.array([[0, 0], [width, 0], [width, height], [0, height]]))
    matrix = cv2.getPerspectiveTransform(corners, destination)
    print(corner_points)
    return cv2.warpPerspective(IMG_ORIGINAL, matrix, (width, height), flags=cv2.INTER_LINEAR)


def add_corner(x: int, y: int):
    global img, corners, WINDOW_NAME, WIDTH, HEIGHT, ALLOW_ORIENTATION_CHANGE, DESTINATION_OUT
    corners.append([x, y])
    if len(corners) == 4:
        corners = perspective.order_points(np.float32(np.array(corners)))
        (width, height) = switch_orientation(WIDTH, HEIGHT) if ALLOW_ORIENTATION_CHANGE else (WIDTH, HEIGHT)
        print(width, height)
        img = transform(width, height, corners)
        corners = []
    else:
        img = cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
    cv2.imshow(WINDOW_NAME, img)


def mouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN and len(corners) < 4:
        add_corner(x, y)


cv2.setMouseCallback(WINDOW_NAME, mouse_callback, (img, path_out, w_out, h_out, allow_orientation_fix))
cv2.imshow(WINDOW_NAME, img)

key = cv2.waitKey(0)
if key == ord('\x1b'):
    print("esc")
    img = IMG_ORIGINAL
elif key == ord('s'):
    print("save")
    cv2.imwrite(DESTINATION_OUT, img)
else:
    cv2.waitKey(0)

