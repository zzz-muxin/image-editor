import cv2
import numpy as np
from PIL import ImageEnhance, Image, ImageFilter
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QPixmap

from tools.image_format import ImageFormat


class Adjust(QObject):
    image_updated = pyqtSignal(QPixmap)  # 图片更新信号

    def __init__(self, pixmap: QPixmap):
        super().__init__()
        self.pixmap = pixmap
        self.image = ImageFormat.pixmap_to_cv(self.pixmap)  # 格式转换
        self.image = self.image[:, :, :3]

    # 设置原始图像
    def set_pixmap(self, pixmap: QPixmap):
        self.pixmap = pixmap
        self.image = ImageFormat.pixmap_to_cv(self.pixmap)  # 格式转换

    # 光感调整
    def adjust_light_perception(self, value):
        # 将图像从 BGR 转换为 HSV
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        # 饱和度因子
        if value >= 0:
            factor_s = 1.0   # [0, 100]映射到[1.0, 1.5]
            factor_v = (value + 100) / 200 * 100 - 50
        else:
            factor_s = 1.0 - value / 100.0 * 0.5  # [-100, 0]映射到[1.5, 1.0]
            factor_v = 0
        image[:, :, 1] = np.clip(image[:, :, 1] * factor_s, 0, 255)
        image[:, :, 2] = np.clip(image[:, :, 2] + factor_v, 0, 255)
        # 将图像从 HSV 转换回 BGR
        image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        self.image_updated.emit(ImageFormat.cv_to_pixmap(image))

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

    # 调整色温
    def adjust_temperature(self, value):
        image = self.image.copy()
        value = (value + 100) / 200.0 * 60 - 30
        if value >= 0:
            image[:, :, 2] = np.clip(image[:, :, 2] + value, 0, 255)  # r
            image[:, :, 1] = np.clip(image[:, :, 1] + value // 2, 0, 255)  # g
            image[:, :, 0] = np.clip(image[:, :, 0] - value // 2, 0, 255)  # b
        else:
            value = abs(value)
            image[:, :, 2] = np.clip(image[:, :, 2] - value, 0, 255)  # r
            image[:, :, 1] = np.clip(image[:, :, 1] - value // 2, 0, 255)  # g
            image[:, :, 0] = np.clip(image[:, :, 0] + value // 2, 0, 255)  # b
        self.image_updated.emit(ImageFormat.cv_to_pixmap(image))

    # 调整色调
    def adjust_hue(self, value):
        image = self.image.copy()
        # 将图像从 BGR 转换为 HSV
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        value = value / 200   # [-100, 100]归一化为[0.5, 1.5]
        image[:, :, 0] = np.clip(image[:, :, 0] + 10 * value, 0, 359)
        # 将图像从 HSV 转换回 BGR
        image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        self.image_updated.emit(ImageFormat.cv_to_pixmap(image))

    # 锐化
    def adjust_sharp(self, value):
        if value != 0:
            value = value / 50.0  # [0, 100]归一化为[0, 2]
            image = self.image.copy()
            pil_image = Image.fromarray(np.uint8(image))  # cv图像转pil图像
            # 进行锐化
            enhancer = ImageEnhance.Sharpness(pil_image)
            img_sharp = enhancer.enhance(factor=value)  # 锐化强度
            cv_image = np.array(img_sharp, dtype=np.uint8)  # pil图像转cv图像
            self.image_updated.emit(ImageFormat.cv_to_pixmap(cv_image))

    # 平滑
    def adjust_smooth(self, value):
        if value != 0:
            value = value / 50.0  # [0, 100]归一化为[0, 2]
            image = self.image.copy()
            pil_image = Image.fromarray(np.uint8(image))  # cv图像转pil图像
            # 应用平均滤波器（Box Blur）进行图像平滑
            smoothed_image = pil_image.filter(ImageFilter.BoxBlur(radius=value))
            cv_image = np.array(smoothed_image, dtype=np.uint8)  # pil图像转cv图像
            self.image_updated.emit(ImageFormat.cv_to_pixmap(cv_image))

    # HSL
    def adjust_h(self, value):
        image = self.image.copy()
        value = value / 200  # [-100, 100]归一化为[0.5, 1.5]
        image_hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)  # BGR转换到HLS
        image_hls[:, :, 0] = np.clip(image_hls[:, :, 0] + 10 * value, 0, 359)
        adjusted_image = cv2.cvtColor(image_hls, cv2.COLOR_HLS2BGR)  # HLS 转换回 BGR
        self.image_updated.emit(ImageFormat.cv_to_pixmap(adjusted_image))

    def adjust_l(self, value):
        image = self.image.copy()
        factor = (value + 100) / 200 * 1 + 0.5  # [-100, 100]归一化为[0.5, 1.5]
        image_hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)  # BGR转换到HLS
        image_hls[:, :, 1] = np.clip(image_hls[:, :, 1] * factor, 0, 255)
        adjusted_image = cv2.cvtColor(image_hls, cv2.COLOR_HLS2BGR)  # HLS 转换回 BGR
        self.image_updated.emit(ImageFormat.cv_to_pixmap(adjusted_image))

    def adjust_s(self, value):
        image = self.image.copy()
        factor = (value + 100) / 200 * 1 + 0.5  # [-100, 100]归一化为[0.5, 1.5]
        image_hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)  # BGR转换到HLS
        image_hls[:, :, 2] = np.clip(image_hls[:, :, 2] * factor, 0, 255)
        adjusted_image = cv2.cvtColor(image_hls, cv2.COLOR_HLS2BGR)  # HLS 转换回 BGR
        self.image_updated.emit(ImageFormat.cv_to_pixmap(adjusted_image))
