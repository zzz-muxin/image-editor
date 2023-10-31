import cv2 as cv
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage


class ImageFormat:
    def __init__(self, image):
        pass

    # PyQt图像 转换为 OpenCV图像
    @staticmethod
    def pixmap_to_cv(pixmap):
        q_image = QPixmap.toImage(pixmap)  # QPixmap 转换为 QImage
        shape = (q_image.height(), q_image.bytesPerLine() * 8 // q_image.depth())
        shape += (4,)
        ptr = q_image.bits()
        ptr.setsize(q_image.byteCount())
        cv_image = np.array(ptr, dtype=np.uint8).reshape(shape)  # 定义 OpenCV 图像
        cv_image = cv_image[..., :3]
        return cv_image

    # OpenCV图像 转换为 PyQt图像
    @staticmethod
    def cv_to_pixmap(image):
        # 8-bits unsigned, NO. OF CHANNELS=1
        row, col, pix = image.shape[0], image.shape[1], image.strides[0]
        channels = 1 if len(image.shape) == 2 else image.shape[2]
        if channels == 3:  # CV_8UC3
            qImg = QImage(image.data, col, row, pix, QImage.Format_RGB888)
            return qImg.rgbSwapped()
        elif channels == 1:
            qImg = QImage(image.data, col, row, pix, QImage.Format_Indexed8)
            return qImg
        else:
            QtCore.qDebug("ERROR: numpy.ndarray could not be converted to QImage. Channels = %d" % image.shape[2])
            return QImage()
