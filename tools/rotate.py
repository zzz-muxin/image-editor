import cv2
import numpy as np
from PyQt5.QtGui import QPixmap

from tools.image_format import ImageFormat

class Rotate:
    def __init__(self, ):
        pass

    @staticmethod
    def rotate_by_slider(pixmap: QPixmap, degree):
        cv_image = ImageFormat.pixmap_to_cv(pixmap)  # 格式转换
        height, width = cv_image.shape[:2]  # 图片的高度和宽度
        x, y = width // 2, height // 2  # 以图像中心作为旋转中心
        # 求出旋转变换矩阵 MAR，三个参数分别为旋转中心，角度，缩放因子
        MAR = cv2.getRotationMatrix2D((x, y), degree, 1.0)
        # 将旋转变换矩阵 MAR应用于图片，使用透明像素填充
        image_rotated = cv2.warpAffine(cv_image, MAR, (width, height), borderValue=(0, 0, 0, 0))
        return ImageFormat.cv_to_pixmap(image_rotated)  # 返回QPixmap格式

    # 旋转角度为90时，直接使用rotate函数，该方法实际上是通过矩阵转置实现的，因此速度很快
    @staticmethod
    def rotate(pixmap: QPixmap, degree: int):
        image_rotated = None
        image = ImageFormat.pixmap_to_cv(pixmap)  # 格式转换
        if degree == 90:
            image_rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif degree == -90:
            image_rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return ImageFormat.cv_to_pixmap(image_rotated)  # 返回QPixmap格式
