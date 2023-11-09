import matplotlib
import cv2

matplotlib.use("Qt5Agg")  # 声明使用pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg  # pyqt5的画布
import matplotlib.pyplot as plt
# matplotlib.figure 模块提供了顶层的Artist(图中的所有可见元素都是Artist的子类)，它包含了所有的plot元素
from matplotlib.figure import Figure
from PyQt5.QtGui import QPixmap
from tools.image_format import ImageFormat

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 解决坐标轴中文显示问题
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号不显示的问题

class GrayHistFigure(FigureCanvasQTAgg):
    # 创建一个画布类，并把画布放到FigureCanvasQTAgg
    def __init__(self, pixmap: QPixmap):
        # plt.rcParams['figure.facecolor'] = 'r'  # 设置窗体颜色
        # plt.rcParams['axes.facecolor'] = 'b'  # 设置绘图区颜色
        # 创建一个Figure,该Figure为matplotlib下的Figure，不是matplotlib.pyplot下面的Figure
        # 这里还要注意，width, height可以直接调用参数，不能用self.width、self.height作为变量获取
        # 因为self.width、self.height 在模块中已经FigureCanvasQTAgg模块中使用，这里定义会造成覆盖
        self.fig = Figure()
        self.pixmap = pixmap
        super(GrayHistFigure, self).__init__(self.fig)  # 在父类中激活self.fig， 否则不能显示图像（就是在画板上放置画布）
        self.ax = self.fig.add_subplot(111)  # 添加绘图区，111表示1行1列，第一张曲线图
        self.draw_figure()

    def draw_figure(self):
        image = ImageFormat.pixmap_to_cv(self.pixmap)  # 格式转换为cv图像
        print(image.shape)
        if image.shape[2] == 4 or image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            print(image.shape)
        gray_hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        self.ax.plot(gray_hist)
        self.ax.set_title('Gray Histogram')  # 表格标题
        self.ax.set_xlabel('gray level')  # x轴标签
        self.ax.set_ylabel('number of pixels')  # y轴标签
        self.ax.set_xlim([0, 256])

class ColorHistFigure(FigureCanvasQTAgg):
    def __init__(self, pixmap: QPixmap):
        self.fig = Figure()
        self.pixmap = pixmap
        super(ColorHistFigure, self).__init__(self.fig)  # 在父类中激活self.fig， 否则不能显示图像（就是在画板上放置画布）
        self.ax = self.fig.add_subplot(111)  # 添加绘图区，111表示1行1列，第一张曲线图
        self.draw_figure()

    def draw_figure(self):
        image = ImageFormat.pixmap_to_cv(self.pixmap)  # 格式转换为cv图像

        self.ax.set_title('Color Histogram')  # 表格标题
        self.ax.set_xlabel('level')  # x轴标签
        self.ax.set_ylabel('number of pixels')  # y轴标签

        colors = ('b', 'g', 'r')
        for i, item in enumerate(colors):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            self.ax.plot(hist, color=item)
            self.ax.set_xlim([0, 256])

