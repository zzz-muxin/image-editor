import cv2
import numpy as np

from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor

from tools.image_format import ImageFormat

# 灰度直方图图表类
class GrayChart(QChartView):
    def __init__(self, pixmap: QPixmap):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿

        self.pixmap = pixmap  # 所需计算直方图的图像
        self.gray_hist = None  # 初始化灰度直方图
        self.line_series = QLineSeries()  # 折线序列
        self.chart = QChart()  # 图表

        # 必须先插入数据再处理图表的轴，否则不会有轴
        self.calculate_histogram()
        self.init_series()
        self.init_chart()

        self.setChart(self.chart)  # 设置QChartView的chart


    # 计算直方图
    def calculate_histogram(self):
        q_image = self.pixmap.toImage()  # QPixmap转换为QImage
        q_image = q_image.convertToFormat(QImage.Format_Grayscale8)  # QImage转换为8位灰度图像
        cv_image = ImageFormat.pixmap_to_cv(QPixmap.fromImage(q_image))  # 转换为cv图像
        # 使用cv2.calcHist计算直方图
        self.gray_hist = cv2.calcHist([cv_image], [0], None, [256], [0, 256])

    # 初始化图表
    def init_chart(self):
        self.chart.addSeries(self.line_series)  # 图表添加折线序列
        self.chart.setTitle("Gray Histogram")  # 表格标题
        self.chart.legend().setVisible(False)  # 设置图例不可见
        #self.chart.setTheme(QChart.ChartThemeDark)  # 表格主题颜色
        self.chart.setAnimationOptions(QChart.SeriesAnimations)  # 启用序列动画

        axis_x = QValueAxis()  # x轴
        #axis_x.setRange(0, 255)  # x轴范围
        axis_x.setLabelFormat("%d")  # x轴使用整数格式显示刻度标签
        #axis_x.setTitleText("pixel value")  # x轴标题
        self.chart.addAxis(axis_x, Qt.AlignBottom)  # 添加x轴到chart底部
        self.line_series.attachAxis(axis_x)  # 关联折线

        axis_y = QValueAxis()  # y轴
        axis_y.setLabelFormat("%d")  # y轴使用整数格式显示刻度标签
        axis_y.setRange(0, max(self.gray_hist)[0])  # y轴限制显示范围
        #axis_y.setTitleText("number of pixels")  # y轴标题
        self.chart.addAxis(axis_y, Qt.AlignLeft)  # 添加y轴到chart左部
        self.line_series.attachAxis(axis_y)  # 关联折线

    # 初始化折线数据
    def init_series(self):
        # 添加直方图数据到表格
        for i in range(256):
            self.line_series.append(i, self.gray_hist[i][0])

    # 更新直方图
    def update_chart(self, new_pixmap: QPixmap):
        self.pixmap = new_pixmap
        self.calculate_histogram()
        # 更新折线系列的数据
        for i in range(256):
            self.line_series.replace(i, i, self.gray_hist[i][0])
        # 强制图表刷新
        self.chart.update()


# rgb直方图图表类
class RGBChart(QChartView):
    def __init__(self, pixmap: QPixmap):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿

        self.pixmap = pixmap  # 所需计算直方图的图像
        # 初始化rgb直方图
        self.red_hist = None
        self.green_hist = None
        self.blue_hist = None
        self.line_series_r = QLineSeries()  # r折线序列
        self.line_series_g = QLineSeries()  # g折线序列
        self.line_series_b = QLineSeries()  # b折线序列
        self.chart = QChart()  # 图表

        # 必须先插入数据再处理图表的轴，否则不会有轴
        self.calculate_histogram()
        self.init_series()
        self.init_chart()

        self.setChart(self.chart)  # 设置QChartView的chart

    # 计算直方图
    def calculate_histogram(self):
        cv_image = ImageFormat.pixmap_to_cv(self.pixmap)  # 转换为cv图像
        # 分别计算三个通道的直方图
        self.red_hist = cv2.calcHist([cv_image], [2], None, [256], [0, 256])
        self.green_hist = cv2.calcHist([cv_image], [1], None, [256], [0, 256])
        self.blue_hist = cv2.calcHist([cv_image], [0], None, [256], [0, 256])

    # 初始化图表
    def init_chart(self):
        # 添加rgb通道折线序列
        self.chart.addSeries(self.line_series_r)
        self.chart.addSeries(self.line_series_g)
        self.chart.addSeries(self.line_series_b)
        self.chart.setTitle("RGB Histogram")  # 表格标题
        self.chart.legend().setVisible(True)  # 设置图例可见
        self.chart.legend().setAlignment(Qt.AlignBottom)  # 设置图例在表格底部
        # self.chart.setTheme(QChart.ChartThemeDark)  # 表格主题颜色
        self.chart.setAnimationOptions(QChart.SeriesAnimations)  # 启用序列动画

        axis_x = QValueAxis()  # x轴
        # axis_x.setRange(0, 255)  # x轴范围
        axis_x.setLabelFormat("%d")  # x轴使用整数格式显示刻度标签
        # axis_x.setTitleText("pixel value")  # x轴标题
        self.chart.addAxis(axis_x, Qt.AlignBottom)  # 添加x轴到chart底部
        # x轴关联rgb折线
        self.line_series_r.attachAxis(axis_x)
        self.line_series_g.attachAxis(axis_x)
        self.line_series_b.attachAxis(axis_x)

        axis_y = QValueAxis()  # y轴
        axis_y.setLabelFormat("%d")  # y轴使用整数格式显示刻度标签
        # 计算三个通道出现的最大频率，y轴限制显示在最大范围内
        red_max_value = max(self.red_hist)[0]
        green_max_value = max(self.green_hist)[0]
        blue_max_value = max(self.blue_hist)[0]
        max_value = max(red_max_value, green_max_value, blue_max_value)
        axis_y.setRange(0, max_value)  # y轴限制显示范围
        # axis_y.setTitleText("number of pixels")  # y轴标题
        self.chart.addAxis(axis_y, Qt.AlignLeft)  # 添加y轴到chart左部
        # y轴关联rgb折线
        self.line_series_r.attachAxis(axis_y)
        self.line_series_g.attachAxis(axis_y)
        self.line_series_b.attachAxis(axis_y)

    # 初始化折线序列
    def init_series(self):
        # 设置rgb折线颜色
        self.line_series_r.setColor(QColor(255, 0, 0))
        self.line_series_g.setColor(QColor(0, 255, 0))
        self.line_series_b.setColor(QColor(0, 0, 255))
        # 设置折线图例文本
        self.line_series_r.setName("Red")
        self.line_series_g.setName("Green")
        self.line_series_b.setName("Blue")
        # 添加直方图数据
        for i in range(256):
            self.line_series_r.append(i, self.red_hist[i][0])
            self.line_series_g.append(i, self.green_hist[i][0])
            self.line_series_b.append(i, self.blue_hist[i][0])


