import cv2
import numpy as np
from PyQt5.QtGui import QPixmap

from tools.image_format import ImageFormat


class Adjust:
    def __init__(self):
        self.pixmap = None
        pass

    def set_pixmap(self, pixmap: QPixmap):
        self.pixmap = pixmap

    def adjust_contrast(self, value):
        image = ImageFormat.pixmap_to_cv(self.pixmap)  # 格式转换
        alpha = 1.0 + value / 100.0
        image_adjust = cv2.convertScaleAbs(image, alpha=alpha, beta=0)

        return ImageFormat.cv_to_pixmap(image_adjust)  # 返回QPixmap格式

    def adjust_brightness(self, value):
        image = ImageFormat.pixmap_to_cv(self.pixmap)  # 格式转换
        image_adjust = cv2.convertScaleAbs(image, alpha=1, beta=value)
        return ImageFormat.cv_to_pixmap(image_adjust)  # 返回QPixmap格式

    # 饱和度调整
    def adjust_saturation(self, value):
        image = ImageFormat.pixmap_to_cv(self.pixmap)  # 格式转换
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # 色彩空间转换, BGR->HSV

        # 调节饱和度的 LUT
        lut = np.array([max(min(i + value, 255), 0) for i in range(256)]).astype(np.uint8)
        hsv[:, :, 1] = cv2.LUT(hsv[:, :, 1], lut)

        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)  # 色彩空间转换, HSV->BGR
        return ImageFormat.cv_to_pixmap(bgr)  # 返回QPixmap格式
