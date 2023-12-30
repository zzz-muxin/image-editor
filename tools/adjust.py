import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QPixmap

from tools.image_format import ImageFormat


class Adjust(QObject):
    image_updated = pyqtSignal(QPixmap)  # 图片更新信号

    def __init__(self, pixmap: QPixmap):
        super().__init__()
        self.pixmap = pixmap
        self.image = ImageFormat.pixmap_to_cv(self.pixmap)  # 格式转换

    # 设置原始图像
    def set_pixmap(self, pixmap: QPixmap):
        self.pixmap = pixmap
        self.image = ImageFormat.pixmap_to_cv(self.pixmap)  # 格式转换

    # 光感调整
    def adjust_light_perception(self, value):
        # todo
        pass

    # 对比度调整
    def adjust_contrast(self, value):
        alpha = (value + 100) / 200 * 1 + 0.5  # [-100, 100]归一化为[0.5, 1.5]
        image = cv2.convertScaleAbs(self.image, alpha=alpha)
        self.image_updated.emit(ImageFormat.cv_to_pixmap(image))

    # 亮度调整
    def adjust_brightness(self, value):
        beta = (value + 100) / 200 * 100 - 50  # [-100, 100]归一化为[-50, 50]
        image = np.clip(self.image + beta, 0, 255).astype(np.uint8)
        self.image_updated.emit(ImageFormat.cv_to_pixmap(image))

    # 曝光调整
    def adjust_exposure(self, value):
        image = self.image
        gamma = 1.5 - (value + 100) * (1 / 200.0)  # [-100, 100]归一化到[1.5, 0.5]
        image = image / 255.0  # 图像归一化到 [0, 1] 范围
        # 应用伽马校正
        image = np.power(image, gamma)
        # 图像缩放回 [0, 255] 范围
        image = (image * 255).astype(np.uint8)
        self.image_updated.emit(ImageFormat.cv_to_pixmap(image))

    # 饱和度调整
    def adjust_saturation(self, value):
        # 将图像从 BGR 转换为 HSV
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        factor = (value + 100) / 200 * 1 + 0.5  # [-100, 100]归一化为[0.5, 1.5]
        image[:, :, 1] = np.clip(image[:, :, 1] * factor, 0, 255)
        # 将图像从 HSV 转换回 BGR
        image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        self.image_updated.emit(ImageFormat.cv_to_pixmap(image))

    #def adjust_apply(self):


