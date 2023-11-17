import cv2
import numpy as np

from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QSplineSeries, QScatterSeries
from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen, QCursor
from PyQt5.QtWidgets import QToolTip
from scipy.interpolate import interp1d

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
        self.spline_points = None

        self.radius = self.scatter_series.markerSize() // 2  # 散点的半径
        self.diameter = self.scatter_series.markerSize()  # 散点的直径
        self.init_series()
        self.init_chart()

        self.scatter_series.hovered.connect(self.on_scatter_hovered)  # 连接鼠标悬停信号
        self.scatter_series.clicked.connect(self.click_scatter)

        self.setChart(self.chart)  # 设置QChartView的chart

    # 初始化图表
    def init_chart(self):
        self.chart.addSeries(self.scatter_series)  # 图表添加散点系列
        self.chart.addSeries(self.line_series)  # 图表添加曲线系列
        self.chart.legend().setVisible(False)  # 设置图例不可见
        # self.chart.setTheme(QChart.ChartThemeDark)  # 表格主题颜色
        # self.chart.setAnimationOptions(QChart.SeriesAnimations)  # 启用系列动画

        self.axis_x.setRange(0, 255)  # x轴显示范围
        self.axis_x.setLabelFormat("%d")  # x轴使用整数格式显示刻度标签
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)  # 添加x轴到chart底部
        self.line_series.attachAxis(self.axis_x)  # 关联折线
        self.scatter_series.attachAxis(self.axis_x)

        self.axis_y.setRange(0, 255)  # y轴显示范围
        self.axis_y.setLabelFormat("%d")  # y轴使用整数格式显示刻度标签
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)  # 添加y轴到chart左部
        self.line_series.attachAxis(self.axis_y)  # 关联折线
        self.scatter_series.attachAxis(self.axis_y)

    # 初始表格数据
    def init_series(self):
        # 添加初始散点
        self.scatter_series.append(0, 0)
        self.scatter_series.append(128, 128)
        self.scatter_series.append(255, 255)
        # 通过spline函数计算散点的样条曲线
        self.spline_points = self.spline(self.scatter_series.pointsVector())
        # 添加计算出的曲线数据点
        for x, y in self.spline_points:
            self.line_series.append(x, y)

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
            if abs(data_point.x() - point.x()) < self.diameter and abs(data_point.y() - point.y()) < self.diameter:
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
                insert_index = 0
                for i, data_point in enumerate(self.scatter_series.pointsVector()):
                    if new_point.x() > data_point.x():
                        insert_index = i + 1
                self.scatter_series.insert(insert_index, new_point)
                self.update_spline()
        print(self.spline_points)

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
            # 要求移动点时不能超过左右两边点的 x 坐标
            if left_point_x + self.radius < point.x() < right_point_x - self.radius:
                self.scatter_series.replace(self.selected_point_index, point)
                self.update_spline()

    def mouseReleaseEvent(self, event):
        self.selected_point_index = None  # 重置鼠标点击选中的点的索引值

    def mouseDoubleClickEvent(self, event):
        pos = event.pos()
        point = self.chart.mapToValue(pos)
        # 检测是否点击在散点附近，使用散点的半径范围
        for i, data_point in enumerate(self.scatter_series.pointsVector()):
            if abs(data_point.x() - point.x()) < self.diameter and abs(data_point.y() - point.y()) < self.diameter:
                # 删除选中的点
                self.scatter_series.remove(i)
                # self.spline_series.remove(i)
                break

    # 根据已知的散点计算出样条曲线
    @staticmethod
    def spline(points: list) -> list:
        point_count = len(points)
        # 提取点的x和y坐标
        x_values = [point.x() for point in points]
        y_values = [point.y() for point in points]
        print(x_values, y_values)
        # 点的个数大于等于4时使用三阶样条曲线，否则使用二阶
        if point_count >= 4:
            kind = 'cubic'
        else:
            kind = 'quadratic'
        # 用scipy的interp1d计算样条插值函数
        spline_function = interp1d(x_values, y_values, kind=kind)
        # 计算插值区间上的整数点
        x_min = int(np.floor(min(x_values)))
        x_max = int(np.ceil(max(x_values)))
        interpolated_points = []  # 返回的列表
        # 遍历x计算其插值y
        for x in range(x_min, x_max + 1):
            interpolated_y = int(spline_function(x))
            # 限制纵坐标在0到255之间
            interpolated_y = min(max(interpolated_y, 0), 255)
            # 添加到结果列表
            interpolated_points.append((x, interpolated_y))

        return interpolated_points

    # 更新样条曲线
    def update_spline(self):
        self.spline_points = self.spline(self.scatter_series.pointsVector())
        for x, y in self.spline_points:
            index = int(x) - int(self.scatter_series.pointsVector()[0].x())
            self.line_series.replace(index, QPointF(float(x), float(y)))

