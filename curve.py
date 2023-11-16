


import cv2

from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QSplineSeries
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor

from tools.image_format import ImageFormat


# 曲线调色类
class Curve(QChartView):
    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿

        self.line_series = QSplineSeries()
        self.chart = QChart()  # 图表
        self.axis_x = QValueAxis()  # x轴
        self.axis_y = QValueAxis()  # y轴

        self.init_series()
        self.init_chart()

        self.setChart(self.chart)  # 设置QChartView的chart

    # 初始化图表
    def init_chart(self):
        self.chart.addSeries(self.line_series)  # 图表添加折线序列
        self.chart.legend().setVisible(False)  # 设置图例不可见
        # self.chart.setTheme(QChart.ChartThemeDark)  # 表格主题颜色
        self.chart.setAnimationOptions(QChart.SeriesAnimations)  # 启用序列动画

        self.axis_x.setLabelFormat("%d")  # x轴使用整数格式显示刻度标签
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)  # 添加x轴到chart底部
        self.line_series.attachAxis(self.axis_x)  # 关联折线

        self.axis_y.setLabelFormat("%d")  # y轴使用整数格式显示刻度标签
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)  # 添加y轴到chart左部
        self.line_series.attachAxis(self.axis_y)  # 关联折线



    # 初始化折线数据
    def init_series(self):
        # 添加直方图数据到表格
        for i in range(256):
            self.line_series.append(i, i)



