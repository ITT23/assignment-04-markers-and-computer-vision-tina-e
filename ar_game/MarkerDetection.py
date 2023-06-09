import cv2
import config
import numpy as np
import cv2.aruco as aruco
from imutils import perspective


class MarkerDetector:
    def __init__(self, init_img):
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
        self.aruco_params = aruco.DetectorParameters()
        self.out_img = init_img
        self.aruco_corners = None

    def detect(self, img):
        """
        detect AruCo Markers and set
        :param img: gray-scaled webcam image
        """
        # Detect ArUco markers in the frame
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, self.aruco_dict, parameters=self.aruco_params)
        # Check if marker is detected
        if ids is not None:
            # Draw lines along the sides of the marker
            # aruco.drawDetectedMarkers(img, corners)
            self.aruco_corners = corners

    def warp(self, img):
        """
        order detected marker points and define game board based on these
        :param img: gray-scaled webcam image
        :return: warp and game board detection successful
        """
        board_corners = []
        if self.aruco_corners and len(self.aruco_corners) == 4:
            for i, corner in enumerate(self.aruco_corners):
                board_corners.append([corner[0][0][0], corner[0][0][1]])
            board_corners_ordered = perspective.order_points((np.array(board_corners)))

            destination = np.float32(np.array([[0, 0], [config.WINDOW_WIDTH, 0], [config.WINDOW_WIDTH, config.WINDOW_HEIGHT], [0, config.WINDOW_HEIGHT]]))
            matrix = cv2.getPerspectiveTransform(board_corners_ordered, destination)
            warped = cv2.warpPerspective(img, matrix, (config.WINDOW_WIDTH, config.WINDOW_HEIGHT), flags=cv2.INTER_LINEAR)
            self.out_img = warped
            # ret, self.out_img = cv2.threshold(warped, 100, 255, cv2.THRESH_BINARY)
            return True
        return False
