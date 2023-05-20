import cv2
import sys
import numpy as np
import math
from imutils import perspective


# read command line parameters
if len(sys.argv) >= 3:
    path_in = sys.argv[1]
    path_out = sys.argv[2]
    try:
        w_out = int(sys.argv[3])
    except:
        w_out = 1080
        print("WARN: No valid input for: output width\nDefault value set.")
    try:
        h_out = int(sys.argv[4])
    except:
        h_out = 1920
        print("WARN: No valid input for: output height\nDefault value set.")
    try:
        allow_orientation_fix = eval(sys.argv[5])
    except:
        allow_orientation_fix = False
        print("WARN: No valid input for: orientation fix allowed\nDefault value set.")
else:
    print("ERROR: Please specify input file and output destination")
    sys.exit(1)


# set constants based on command line parameters
WIDTH = w_out
HEIGHT = h_out
ALLOW_ORIENTATION_CHANGE = allow_orientation_fix
DESTINATION_OUT = path_out
WINDOW_NAME = 'Preview Window'
IMG_ORIGINAL = cv2.imread(path_in)


def switch_orientation(width: int, height: int):
    """
    switch width and height to better match selected region
    :param width: width before switch
    :param height: height before switch
    :return: updated width and height after switch where necessary
    """
    dx_upper = math.sqrt((corners[0][0] - corners[1][0]) ** 2 + (corners[0][1] - corners[1][1]) ** 2)
    dx_lower = math.sqrt((corners[3][0] - corners[2][0]) ** 2 + (corners[3][1] - corners[2][1]) ** 2)
    dy_left = math.sqrt((corners[0][0] - corners[3][0]) ** 2 + (corners[0][1] - corners[3][1]) ** 2)
    dy_right = math.sqrt((corners[1][0] - corners[2][0]) ** 2 + (corners[1][1] - corners[2][1]) ** 2)

    if (max([dx_upper, dx_lower]) < max([dy_left, dy_right]) and width > height) or (
            max([dx_upper, dx_lower]) > max([dy_left, dy_right]) and width < height):
        return height, width
    return width, height


def transform(width: int, height: int):
    """
    perspective transformation to given width and height
    :param width: width to transform to
    :param height: height to transform to
    :return: warped image
    """
    global img_result, corners
    destination = np.float32(np.array([[0, 0], [width, 0], [width, height], [0, height]]))
    matrix = cv2.getPerspectiveTransform(corners, destination)
    return cv2.warpPerspective(img_result, matrix, (width, height), flags=cv2.INTER_LINEAR)


def add_corner(x: int, y: int):
    """
    add corner on click, initiate transformation on 4th corner clicked
    :param x: x corner
    :param y: y corner
    """
    global img, corners, is_result_displayed, WINDOW_NAME, WIDTH, HEIGHT, ALLOW_ORIENTATION_CHANGE, DESTINATION_OUT
    corners.append([x, y])
    if len(corners) == 4:
        corners = perspective.order_points(np.float32(np.array(corners)))
        (width, height) = switch_orientation(WIDTH, HEIGHT) if ALLOW_ORIENTATION_CHANGE else (WIDTH, HEIGHT)
        img = transform(width, height)
        cv2.imshow(WINDOW_NAME, img)
        is_result_displayed = True
        corners = []
    else:
        img = cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
        cv2.imshow(WINDOW_NAME, img)
        is_result_displayed = False


def mouse_callback(event, x, y, flags, params):
    # prevent adding corners in result view as well as if there are already 4 corners
    if event == cv2.EVENT_LBUTTONDOWN and len(corners) < 4 and not is_result_displayed:
        add_corner(x, y)


is_result_displayed = False
corners = []

img = IMG_ORIGINAL.copy()
img_result = IMG_ORIGINAL.copy()
cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(WINDOW_NAME, mouse_callback, (img, path_out, w_out, h_out, allow_orientation_fix))
cv2.imshow(WINDOW_NAME, img)


if __name__ == '__main__':
    while True:
        key = cv2.waitKey(0)
        # on esc: discard changes and show original img
        if key == ord('\x1b'):
            corners.clear()
            img = IMG_ORIGINAL.copy()
            cv2.imshow(WINDOW_NAME, img)
            is_result_displayed = False
        # on s: if in result view: save image
        elif key == ord('s') and is_result_displayed:
            cv2.imwrite(DESTINATION_OUT, img)
        # on q: quit
        elif key == ord('q'):
            break
    sys.exit(0)
