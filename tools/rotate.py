import cv2
import numpy as np
from PyQt5.QtGui import QPixmap

from tools.image_format import ImageFormat


class Rotate:
    def __init__(self):
        # self.pixmap = None
        pass

    # def set_pixmap(self, pixmap: QPixmap):
    #     self.pixmap = pixmap

    # 自由旋转需要确保图片不会被裁剪，保证图片完整
    # def rotate_by_slider(self, degree):
    #     cv_image = ImageFormat.pixmap_to_cv(self.pixmap)  # 格式转换
    #     height, width = cv_image.shape[:2]  # 图片的高度和宽度
    #     center_x, center_y = width / 2, height / 2  # 以图像中心作为旋转中心
    #     # 求出旋转变换矩阵 MAR，三个参数分别为旋转中心，角度，缩放因子
    #     MAR = cv2.getRotationMatrix2D((center_x, center_y), degree, 1.0)
    #
    #     # 获取矩阵cos和sin绝对值（矩阵的旋转分量）
    #     cos = np.abs(MAR[0, 0])
    #     sin = np.abs(MAR[0, 1])
    #     # 计算旋转后的新高度和宽度
    #     new_width = int((height * sin) + (width * cos))
    #     new_height = int((height * cos) + (width * sin))
    #     # 调整旋转矩阵以考虑图像平移
    #     MAR[0, 2] += (new_width / 2) - center_x
    #     MAR[1, 2] += (new_height / 2) - center_y
    #
    #     # 将旋转变换矩阵MAR应用于图片，使用透明像素填充
    #     image_rotated = cv2.warpAffine(cv_image, MAR, (new_width, new_height), borderValue=(0, 0, 0, 0))
    #     return ImageFormat.cv_to_pixmap(image_rotated)  # 返回QPixmap格式

    # 旋转角度为90时，直接使用cv2.rotate函数，该方法实际上是通过矩阵转置实现的，因此速度很快
    @staticmethod
    def rotate(pixmap: QPixmap, degree: int):
        image_rotated = None
        image = ImageFormat.pixmap_to_cv(pixmap)  # 格式转换
        if degree == 90:
            image_rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif degree == -90:
            image_rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return ImageFormat.cv_to_pixmap(image_rotated)  # 返回QPixmap格式
