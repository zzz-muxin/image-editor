import cv2
import numpy as np
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPixmap

from tools.image_format import ImageFormat


class Crop:
    def __init__(self):
        pass

    # 用QRect裁剪QPixmap
    # 裁剪实际上只是拷贝某块区域的像素
    @staticmethod
    def crop_image(pixmap: QPixmap, rect: QRectF):
        x = int(rect.x())
        y = int(rect.y())
        width = int(rect.width())
        height = int(rect.height())
        image_original = ImageFormat.pixmap_to_cv(pixmap)  # 格式转换
        print("image:", image_original.shape)
        image_cropped = image_original[y:y + height, x:x + width].copy()  # 用copy()进行深拷贝
        print("image_cropped:", image_cropped.shape)
        return ImageFormat.cv_to_pixmap(image_cropped)

