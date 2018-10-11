from typing import Tuple, T

import cv2 as cv
import numpy as np


class Image:
    def __init__(self, img, name):
        self.img = img
        self.name = name

        self._edges = None

    @property
    def edges(self, threshold: Tuple = (150, 250)):
        if self._edges is None:
            edge_img = cv.Canny(self.img, threshold[0], threshold[1])
            edge_name = '{0}_edges'.format(self.name)
            self._edges = ImageFromMatrix(edge_img, edge_name)
        return self._edges

    def resize_to_match(self, image: T, height=False, width=False):
        new_height = image.height() if height else self.height()
        new_width = image.width if width else self.width()
        self.img = cv.resize(self.img, (new_width, new_height))

    def height(self):
        return self.img.shape[0]

    def width(self):
        return self.img.shape[1]

    def overlay(self, image: T, alpha: float, beta: float, x: int, y: int):
        if x + image.width() > self.width() or x < 0 or y + image.height() > self.height() or y < 0:
            print("{0} is overlaid on {1} out of frame. "
                                 "Dimensions of {1} are ({2}, {3}), {0} was placed at ({4}, {5})".format(image.name,
                                                                                                         self.name,
                                                                                                         self.width(),
                                                                                                         self.height(),
                                                                                                         x, y))

        img = np.copy(self.img)
        x_start = max(0, x)
        x_stop = min(x + image.width(), self.width())
        y_start = max(0, y)
        y_stop = min(y + image.height(), self.height())
        for x_i in range(x_start, x_stop):
            for y_i in range(y_start, y_stop):
                img[y_i, x_i] = alpha * img[y_i, x_i] + beta * image.img[y_i - y, x_i - x]

        return ImageFromMatrix(img, "overlay_{0}_on_{1}_at_{2}_{3}".format(image.name, self.name, x, y))

    def set_num_channels(self, n):
        if n <= 0:
            raise ValueError("The image can only have 1 channel (grayscale) or 3 channels (RGB)")

        if n == 1:
            self.img = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)  # make the vbar 1-channel
        elif n == 3:
            self.img = cv.cvtColor(self.img, cv.COLOR_GRAY2BGR)  # make the vbar 1-channel
        else:
            raise ValueError("Unsupported number of channels: {0}".format(n))

class ImageFromPath(Image):
    def __init__(self, path: str):
        img = cv.imread(path)
        if img is None:
            raise ValueError("No image found at {0}".format(path))
        extension_start = path.rfind('.')
        name = path[:extension_start]
        super().__init__(img, name)


class ImageFromMatrix(Image):
    def __init__(self, img, name: str):
        super().__init__(img, name)
