
import cv2

from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QSplineSeries, QScatterSeries
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen, QCursor
from PyQt5.QtWidgets import QToolTip

from tools.image_format import ImageFormat


# 曲线调色类
class Curve(QChartView):
    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿

        self.line_series = QLineSeries()  # 样条曲线系列
        self.scatter_series = QScatterSeries()  # 散点图系列
        self.chart = QChart()  # 图表
        self.axis_x = QValueAxis()  # x轴
        self.axis_y = QValueAxis()  # y轴
        self.selected_point_index = None  # 鼠标点击选中的散点的索引值

        self.tolerance = self.scatter_series.markerSize()  # 散点的半径作为鼠标点击的误差值范围
        self.init_series()
        self.init_chart()

        self.scatter_series.hovered.connect(self.on_scatter_hovered)  # 连接鼠标悬停信号
        self.scatter_series.clicked.connect(self.click_scatter)

        self.setChart(self.chart)  # 设置QChartView的chart

    # 初始化图表
    def init_chart(self):
        self.chart.addSeries(self.line_series)  # 图表添加折线系列
        self.chart.addSeries(self.scatter_series)  # 图表添加散点系列
        self.chart.legend().setVisible(False)  # 设置图例不可见
        # self.chart.setTheme(QChart.ChartThemeDark)  # 表格主题颜色
        #self.chart.setAnimationOptions(QChart.SeriesAnimations)  # 启用系列动画

        self.axis_x.setRange(0, 255)  # x轴显示范围
        self.axis_x.setLabelFormat("%d")  # x轴使用整数格式显示刻度标签
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)  # 添加x轴到chart底部
        self.line_series.attachAxis(self.axis_x)  # 关联折线

        self.axis_y.setRange(0, 255)  # y轴显示范围
        self.axis_y.setLabelFormat("%d")  # y轴使用整数格式显示刻度标签
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)  # 添加y轴到chart左部
        self.line_series.attachAxis(self.axis_y)  # 关联折线

    # 初始化折线数据
    def init_series(self):
        self.line_series.append(0, 0)
        self.line_series.append(128, 128)
        self.line_series.append(255, 255)
        self.scatter_series.append(0, 0)
        self.scatter_series.append(128, 128)
        self.scatter_series.append(255, 255)
        # self.scatter_series.setPen(QColor(0, 0, 0))
        # self.scatter_series.setBrush(QColor(255, 255, 255))

    # 鼠标悬停在散点上时显示坐标
    @staticmethod
    def on_scatter_hovered(point):
        QToolTip.showText(QCursor.pos(), f'({int(point.x())}, {int(point.y())})')

    def click_scatter(self, point):
        print(int(point.x()), int(point.y()))
        pass


    def mousePressEvent(self, event):
        pos = event.pos()
        point = self.chart.mapToValue(pos)  # 映射到图表上的坐标
        point = QPoint(int(point.x()), int(point.y()))  # 将坐标转换为整数类型

        # 检测是否点击在散点附近，使用散点的半径范围
        for i, data_point in enumerate(self.scatter_series.pointsVector()):
            if abs(data_point.x() - point.x()) < self.tolerance and abs(data_point.y() - point.y()) < self.tolerance:
                self.selected_point_index = i
                print(data_point.x(), data_point.y())
                break

        # 判断鼠标点击位置是否在坐标轴范围内
        x_in_range = 0 <= point.x() <= 255
        y_in_range = 0 <= point.y() <= 255
        # 新建一个散点
        if self.selected_point_index is None and x_in_range and y_in_range:
            existing_x_values = {point.x() for point in self.scatter_series.pointsVector()}
            if point.x() not in existing_x_values:
                new_point = QPoint(int(point.x()), int(point.y()))
                print(new_point.x(), new_point.y())
                # 找到插入的位置
                insert_index = None
                for i, data_point in enumerate(self.scatter_series.pointsVector()):
                    if new_point.x() > data_point.x():
                        insert_index = i + 1
                self.scatter_series.insert(insert_index, new_point)
                self.line_series.insert(insert_index, new_point)


    def mouseMoveEvent(self, event):
        pos = event.pos()
        point = self.chart.mapToValue(pos)  # 映射到图表上的坐标
        point = QPoint(int(point.x()), int(point.y()))  # 将坐标转换为整数类型
        # 判断鼠标点击位置是否在坐标轴范围内
        x_in_range = 0 <= point.x() <= 255
        y_in_range = 0 <= point.y() <= 255
        if self.selected_point_index is not None and x_in_range and y_in_range:
            # 获取左右两边点的 x 坐标
            left_point_x = self.scatter_series.pointsVector()[
                self.selected_point_index - 1].x() if self.selected_point_index > 0 else 0
            right_point_x = self.scatter_series.pointsVector()[
                self.selected_point_index + 1].x() if self.selected_point_index < len(
                self.scatter_series.pointsVector()) - 1 else 255
            # 要求移动点时不能超过左右两边点的 x 坐标，保证曲线具有一对一的函数性质
            if left_point_x < point.x() < right_point_x:
                self.scatter_series.replace(self.selected_point_index, point)
                self.line_series.replace(self.selected_point_index, point)


    def mouseReleaseEvent(self, event):
        self.selected_point_index = None  # 重置鼠标点击选中的点的索引值

    def mouseDoubleClickEvent(self, event):
        pos = event.pos()
        point = self.chart.mapToValue(pos)
        # 检测是否点击在散点附近，使用散点的半径范围
        for i, data_point in enumerate(self.scatter_series.pointsVector()):
            if abs(data_point.x() - point.x()) < self.tolerance and abs(data_point.y() - point.y()) < self.tolerance:
                # 删除选中的点
                self.scatter_series.remove(i)
                self.line_series.remove(i)
                break

