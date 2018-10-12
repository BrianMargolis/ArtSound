from typing import Tuple, T

import cv2 as cv
import numpy as np


class Image:
    def __init__(self, img, name):
        self.img = img
        self.name = name

        self._edges = None

    def edge_detection(self, threshold: Tuple = (150, 250)):
        edge_img = cv.Canny(self.img, threshold[0], threshold[1])
        edge_name = '{0}_edges'.format(self.name)
        cv.imwrite(edge_name + ".png", edge_img)
        self._edges = ImageFromMatrix(edge_img, edge_name)

    @property
    def edges(self):
        if self._edges is None:
            raise RuntimeError("Edges were not generated for image {0}. Call edge_detection() first.".format(self.name))
        else:
            return self._edges

    def resize_to_match(self, image: T, height=False, width=False):
        new_height = image.height() if height else self.height()
        new_width = image.width if width else self.width()
        self.img = cv.resize(self.img, (new_width, new_height))

    def height(self) -> int:
        return self.img.shape[0]

    def width(self) -> int:
        return self.img.shape[1]

    def overlay(self, image: T, alpha: float, beta: float, x: int, y: int) -> T:
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

    def to_grayscale(self):
        if not self.is_grayscale:
            self.img = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)

    def to_bgr(self):
        if self.is_grayscale:
            self.img = cv.cvtColor(self.img, cv.COLOR_GRAY2BGR)

    @property
    def is_grayscale(self):
        return len(self.img.shape) == 2


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
