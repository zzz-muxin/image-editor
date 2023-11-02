import cv2
import numpy as np
from PyQt5.QtGui import QPixmap

from tools.image_format import ImageFormat


class Flip:
    def __init__(self):
        pass

    # 水平镜像
    @staticmethod
    def flip_x(pixmap: QPixmap):
        image = ImageFormat.pixmap_to_cv(pixmap)  # 格式转换
        image_flip_x = cv2.flip(image, 1)
        return ImageFormat.cv_to_pixmap(image_flip_x)  # 返回QPixmap格式

    # 垂直镜像
    @staticmethod
    def flip_y(pixmap: QPixmap):
        image = ImageFormat.pixmap_to_cv(pixmap)  # 格式转换
        image_flip_y = cv2.flip(image, 0)
        return ImageFormat.cv_to_pixmap(image_flip_y)  # 返回QPixmap格式
