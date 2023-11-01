import cv2 as cv
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage

'''
    OpenCV 按B/G/R顺序存储为ndarray多维数组，
    而PyQt、Matplotlib 等库使用的是 R/G/B 格式。
    因此，将OpenCV彩色图像转换为QImage时,要进行颜色通道的顺序调换
'''

class ImageFormat:
    def __init__(self):
        pass

    # PyQt图像 转换为 OpenCV图像
    @staticmethod
    def pixmap_to_cv(pixmap: QPixmap):
        q_image = QPixmap.toImage(pixmap)  # QPixmap 转换为 QImage
        channels = None
        if q_image.depth() == 32:
            # 32位深的图像通道数为4（rgba）
            channels = 4
        elif q_image.depth() == 24:
            # 24位深的图像通道数为3（rgb）
            channels = 3
        elif q_image.depth() == 8:
            # 8位深的图像通道数为1（灰度图像）
            channels = 1
        else:
            QtCore.qDebug("ERROR: QPixmap.channels could not be converted to cv_image")
        # 构造shape：图像栅格的行数（高度）、列数（宽度）、通道数
        # 每行像素的总位数 整除 像素的位深度 = 每行像素的像素数量（宽度）
        shape = (q_image.height(), q_image.bytesPerLine() * 8 // q_image.depth())
        # 获取QImage通道数
        shape += (channels,)
        # 获取一个指向图像数据的 QByteArray 指针，其中包含了图像的像素信息
        ptr = q_image.bits()
        # 将指针的大小设置为与图像数据的总字节数相等，确保指针具有足够的内存来容纳整个图像数据
        ptr.setsize(q_image.byteCount())
        # 将 ptr 中的指针数据转换为 ndarray 数组，数据类型为无符号8位整数 (np.uint8)，
        # 并使用 reshape 方法将 ndarray 数组重新构造为shape形状
        cv_image = np.array(ptr, dtype=np.uint8).reshape(shape)  # 定义 OpenCV 图像
        return cv_image  # 返回一个ndarray数组

    # OpenCV图像 转换为 PyQt图像
    @staticmethod
    def cv_to_pixmap(cv_image):
        try:
            # 图像栅格的行数（高度）、列数（宽度）、像素行之间的字节间隔
            row, col, pix = cv_image.shape[0], cv_image.shape[1], cv_image.strides[0]
            # 灰色图像channels = 1，彩色图像channels = 3
            channels = 1 if len(cv_image.shape) == 2 else cv_image.shape[2]
            if channels == 3:
                # CV_8UC3  3通道8位无符号整数格式的矩阵
                # 图像以24位RGB格式（8-8-8）存储，并将opencv的RGB格式转BGR格式
                q_image = QImage(cv_image.data, col, row, pix, QImage.Format_RGB888).rgbSwapped()
                return QPixmap.fromImage(q_image)
            elif channels == 4:
                # 图像使用32位字节顺序RGBA格式（8-8-8-8）的预乘透明度格式存储
                try:
                    q_image = QImage(cv_image.data, col, row, pix, QImage.Format_RGBA8888_Premultiplied).rgbSwapped()
                    return QPixmap.fromImage(q_image)
                except Exception as e:
                    print("Error:", e)
            elif channels == 1:
                # 灰度图像使用8位灰度格式存储
                q_image = QImage(cv_image.data, col, row, pix, QImage.Format_Grayscale8)
                return QPixmap.fromImage(q_image)
            else:
                QtCore.qDebug("ERROR: numpy.ndarray could not be converted to QImage. Channels = %d"
                              % cv_image.shape[2])
                return QPixmap.fromImage(QImage())
        except Exception as e:
            print("Error:", e)
