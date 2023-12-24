import numpy as np
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QSplineSeries, QScatterSeries
from PyQt5.QtCore import Qt, QPoint, QPointF, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor
from scipy.interpolate import interp1d

from tools.image_format import ImageFormat


# 曲线调色类
class Curve(QChartView):
    image_updated = pyqtSignal(QPixmap)  # 图片更新信号

    def __init__(self, pixmap: QPixmap):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿
        self.pixmap = pixmap  # 原始图像
        self.chart = QChart()  # 图表
        self.axis_x = QValueAxis()  # x轴
        self.axis_y = QValueAxis()  # y轴
        self.line_series_rgb = QSplineSeries()  # 样条曲线系列
        self.line_series_r = QSplineSeries()
        self.line_series_g = QSplineSeries()
        self.line_series_b = QSplineSeries()
        self.scatter_series_rgb = QScatterSeries()  # 散点图系列
        self.scatter_series_r = QScatterSeries()
        self.scatter_series_g = QScatterSeries()
        self.scatter_series_b = QScatterSeries()
        self.selected_point_index = None  # 鼠标点击选中的散点的索引值
        self.spline_points_rgb = None  # rgb曲线数据点集
        self.spline_points_r = None  # red曲线数据点集
        self.spline_points_g = None  # green曲线数据点集
        self.spline_points_b = None  # blue曲线数据点集
        self.diameter = self.scatter_series_rgb.markerSize()  # 散点的直径

        self.init_series()  # 初始化系列
        self.init_chart()  # 初始化图表

        # self.scatter_series.hovered.connect(self.on_scatter_hovered)  # 连接鼠标悬停信号
        # self.scatter_series.clicked.connect(self.click_scatter)

        self.setChart(self.chart)  # 设置QChartView的chart

    # 初始化图表
    def init_chart(self):
        # 必须先插入系列数据再处理图表的轴，否则不会有轴
        self.chart.addSeries(self.line_series_rgb)  # 图表添加曲线系列
        self.chart.addSeries(self.line_series_r)
        self.chart.addSeries(self.line_series_g)
        self.chart.addSeries(self.line_series_b)
        self.chart.addSeries(self.scatter_series_rgb)  # 图表添加散点系列
        self.chart.addSeries(self.scatter_series_r)
        self.chart.addSeries(self.scatter_series_g)
        self.chart.addSeries(self.scatter_series_b)
        self.chart.legend().setVisible(False)  # 设置图例不可见
        self.axis_x.setRange(0, 255)  # x轴显示范围
        self.axis_x.setLabelFormat("%d")  # x轴使用整数格式显示刻度标签
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)  # 添加x轴到chart底部
        self.axis_y.setRange(0, 255)  # y轴显示范围
        self.axis_y.setLabelFormat("%d")  # y轴使用整数格式显示刻度标签
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)  # 添加y轴到chart左部

    # 初始表格数据系列
    def init_series(self):
        # 设置各曲线和散点画笔颜色
        self.scatter_series_rgb.setPen(QColor(0, 0, 0))
        self.scatter_series_rgb.setBrush(QColor(255, 255, 255))
        self.scatter_series_r.setPen(QColor(240, 0, 0))
        self.scatter_series_r.setBrush(QColor(255, 255, 255))
        self.scatter_series_g.setPen(QColor(33, 255, 53))
        self.scatter_series_g.setBrush(QColor(255, 255, 255))
        self.scatter_series_b.setPen(QColor(2, 132, 252))
        self.scatter_series_b.setBrush(QColor(255, 255, 255))
        self.line_series_rgb.setPen(QColor(0, 0, 0))
        self.line_series_r.setPen(QColor(240, 0, 0))
        self.line_series_g.setPen(QColor(33, 255, 53))
        self.line_series_b.setPen(QColor(2, 132, 252))
        # 添加初始散点
        default_points = [QPointF(0, 0), QPointF(255, 255)]
        for point in default_points:
            self.scatter_series_rgb.append(point)
            self.scatter_series_r.append(point)
            self.scatter_series_g.append(point)
            self.scatter_series_b.append(point)
        # 通过spline函数计算散点的样条曲线数据
        self.spline_points_rgb = self.spline(self.scatter_series_rgb.pointsVector())
        self.spline_points_r = self.spline(self.scatter_series_r.pointsVector())
        self.spline_points_g = self.spline(self.scatter_series_g.pointsVector())
        self.spline_points_b = self.spline(self.scatter_series_b.pointsVector())
        # 添加计算出的曲线数据点绘制到图表
        for x, y in self.spline_points_rgb:
            self.line_series_rgb.append(x, y)
        for x, y in self.spline_points_r:
            self.line_series_r.append(x, y)
        for x, y in self.spline_points_g:
            self.line_series_g.append(x, y)
        for x, y in self.spline_points_b:
            self.line_series_b.append(x, y)
        # 初始时设置单通道的数据不可见
        self.line_series_r.setVisible(False)
        self.line_series_g.setVisible(False)
        self.line_series_b.setVisible(False)
        self.scatter_series_r.setVisible(False)
        self.scatter_series_g.setVisible(False)
        self.scatter_series_b.setVisible(False)

    # 鼠标悬停在散点上时显示坐标
    # @staticmethod
    # def on_scatter_hovered(point):
    #     QToolTip.showText(QCursor.pos(), f'({int(point.x())}, {int(point.y())})')

    # def click_scatter(self, point):
    #     print(int(point.x()), int(point.y()))
    #     pass

    # 找到当前处理的散点系列current_series
    def find_current_series(self):
        if self.scatter_series_r.isVisible():
            current_series = self.scatter_series_r
        elif self.scatter_series_g.isVisible():
            current_series = self.scatter_series_g
        elif self.scatter_series_b.isVisible():
            current_series = self.scatter_series_b
        else:
            current_series = self.scatter_series_rgb
        return current_series

    # 重写鼠标点击事件
    def mousePressEvent(self, event):
        current_series = self.find_current_series()  # 当前处理的散点系列
        pos = event.pos()
        point = self.chart.mapToValue(pos)  # 映射到图表上的坐标
        point = QPoint(int(point.x()), int(point.y()))  # 将坐标转换为整数类型
        # 左键点击实现新增散点
        if event.button() == Qt.LeftButton:
            # 检测是否点击在散点附近
            for i, data_point in enumerate(current_series.pointsVector()):
                if abs(data_point.x() - point.x()) < self.diameter and abs(data_point.y() - point.y()) < self.diameter:
                    self.selected_point_index = i
                    break
            # 判断鼠标点击位置是否在坐标轴范围内
            x_in_range = 0 <= point.x() <= 255
            y_in_range = 0 <= point.y() <= 255
            # 新建一个散点
            if self.selected_point_index is None and x_in_range and y_in_range:
                existing_x_values = {point.x() for point in current_series.pointsVector()}
                if point.x() not in existing_x_values:
                    new_point = QPoint(int(point.x()), int(point.y()))
                    # 找到插入的位置
                    insert_index = 0
                    for i, data_point in enumerate(current_series.pointsVector()):
                        if new_point.x() > data_point.x():
                            insert_index = i + 1
                    current_series.insert(insert_index, new_point)
                    self.update_line_series()
        # 右键点击实现去除散点
        if event.button() == Qt.RightButton:
            # 只有点的个数大于2才能删除
            if current_series.count() > 2:
                # 检测是否点击在散点附近
                for i, data_point in enumerate(current_series.pointsVector()):
                    if abs(data_point.x() - point.x()) < self.diameter and abs(
                            data_point.y() - point.y()) < self.diameter:
                        # 删除选中的点
                        current_series.remove(i)
                        self.update_line_series()
                        break

    # 重写鼠标移动事件
    def mouseMoveEvent(self, event):
        current_series = self.find_current_series()  # 当前处理的散点系列
        pos = event.pos()
        point = self.chart.mapToValue(pos)  # 映射到图表上的坐标
        point = QPoint(int(point.x()), int(point.y()))  # 将坐标转换为整数类型
        # 判断鼠标移动位置是否在坐标轴范围内
        x_in_range = 0 <= point.x() <= 255
        y_in_range = 0 <= point.y() <= 255
        if self.selected_point_index is not None and x_in_range and y_in_range:
            # 获取左右两边点的 x 坐标
            left_point_x = current_series.pointsVector()[
                self.selected_point_index - 1].x() if self.selected_point_index > 0 else 0
            right_point_x = current_series.pointsVector()[
                self.selected_point_index + 1].x() if self.selected_point_index < len(
                current_series.pointsVector()) - 1 else 255
            # 限制移动点时不能超过左右两边点的 x 坐标
            if left_point_x < point.x() < right_point_x:
                current_series.replace(self.selected_point_index, point)
                self.update_line_series()

    # 重写鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.selected_point_index = None  # 重置鼠标点击选中的点的索引值
        self.curve_apply()

    # 根据散点计算出样条曲线数据
    @staticmethod
    def spline(points: list) -> list:
        point_count = len(points)
        # 提取点的x和y坐标
        x_values = [point.x() for point in points]
        y_values = [point.y() for point in points]
        # 点的个数大于等于4时使用三阶样条曲线
        if point_count >= 4:
            kind = 'cubic'
        # 点的个数等于3时使用二阶样条曲线
        elif point_count == 3:
            kind = 'quadratic'
        # 点的个数小于3时使用线性曲线
        else:
            kind = 'linear'
        # 用scipy的interp1d函数计算样条插值函数
        spline_function = interp1d(x_values, y_values, kind=kind)
        # 计算插值区间上的整数点
        x_min = int(np.floor(min(x_values)))
        x_max = int(np.ceil(max(x_values)))
        interpolated_points = []  # 返回的插值列表
        # 遍历x计算其插值y
        for x in range(x_min, x_max + 1):
            interpolated_y = int(spline_function(x))
            # 限制纵坐标在0到255之间
            interpolated_y = min(max(interpolated_y, 0), 255)
            # 添加到结果列表
            interpolated_points.append((x, interpolated_y))
        # 返回一个计算出的样条曲线的整数点集
        return interpolated_points

    # 更新样条曲线系列数据
    def update_line_series(self):
        current_scatter_series = self.find_current_series()
        # 根据当前散点系列找到对应的样条曲线系列，并清空对应的样条曲线系列数据点，准备重绘
        if current_scatter_series == self.scatter_series_r:
            current_spline_points = self.spline_points_r
            current_line_series = self.line_series_r
            self.spline_points_r.clear()
            self.line_series_r.clear()
        elif current_scatter_series == self.scatter_series_g:
            current_spline_points = self.spline_points_g
            current_line_series = self.line_series_g
            self.spline_points_g.clear()
            self.line_series_g.clear()
        elif current_scatter_series == self.scatter_series_b:
            current_spline_points = self.spline_points_b
            current_line_series = self.line_series_b
            self.spline_points_b.clear()
            self.line_series_b.clear()
        else:
            current_spline_points = self.spline_points_rgb
            current_line_series = self.line_series_rgb
            self.spline_points_rgb.clear()
            self.line_series_rgb.clear()
        points = self.spline(current_scatter_series.pointsVector())  # 重新计算样条曲线数据点
        first_point = current_scatter_series.at(0)  # 获取第一个数据点
        last_point = current_scatter_series.at(current_scatter_series.count() - 1)  # 获取最后一个数据点
        # 如果第一个点横坐标不是0，则填充0到第一个点区间上的数据
        if first_point.x() != 0:
            for x in range(0, int(first_point.x())):
                points.insert(x, (x, int(first_point.y())))
        # 如果最后一个点横坐标不是255，则填充最后一个点到255区间上的数据
        if last_point.x() != 255:
            for x in range(int(last_point.x()) + 1, 256):
                points.insert(x, (x, int(last_point.y())))
        # 将计算出的样条曲线数据点添加到series
        for x, y in points:
            current_spline_points.append((x, y))
            current_line_series.append(QPointF(float(x), float(y)))

    # 应用曲线到图片
    def curve_apply(self):
        cv_image = ImageFormat.pixmap_to_cv(self.pixmap)  # 获取原始图像转换为cv图像
        height, width, _ = cv_image.shape  # 获取图像宽高
        # 遍历图像的每个像素点
        for y in range(height):
            for x in range(width):
                # 获取图像当前像素点的 RGB 值，注意opencv中是BGR
                b = cv_image[y, x][0]
                g = cv_image[y, x][1]
                r = cv_image[y, x][2]
                # 将图像的 RGB 值替换为样条曲线上的对应值
                # 先对rgb单通道分别调整
                r = self.spline_points_r[r][1]
                g = self.spline_points_g[g][1]
                b = self.spline_points_b[b][1]
                # 再对rgb混合通道调整
                r = self.spline_points_rgb[r][1]
                g = self.spline_points_rgb[g][1]
                b = self.spline_points_rgb[b][1]
                cv_image[y, x][0] = b
                cv_image[y, x][1] = g
                cv_image[y, x][2] = r
        new_pixmap = ImageFormat.cv_to_pixmap(cv_image)  # 更新图像
        self.image_updated.emit(new_pixmap)  # 发射图片更新信号

    # 设置各系列可见性
    def set_series_visibility(self, rgb_visible, r_visible, g_visible, b_visible):
        self.line_series_rgb.setVisible(rgb_visible)
        self.scatter_series_rgb.setVisible(rgb_visible)
        self.line_series_r.setVisible(r_visible)
        self.line_series_g.setVisible(g_visible)
        self.line_series_b.setVisible(b_visible)
        self.scatter_series_r.setVisible(r_visible)
        self.scatter_series_g.setVisible(g_visible)
        self.scatter_series_b.setVisible(b_visible)
        # 混合通道曲线可见时，单通道曲线也可见
        if rgb_visible is True:
            self.line_series_r.setVisible(True)
            self.line_series_g.setVisible(True)
            self.line_series_b.setVisible(True)

    # 点击彩色按钮
    def click_colorful_button(self):
        self.set_series_visibility(True, False, False, False)

    # 点击红色按钮
    def click_red_button(self):
        self.set_series_visibility(False, True, False, False)

    # 点击绿色按钮
    def click_green_button(self):
        self.set_series_visibility(False, False, True, False)

    # 点击蓝色按钮
    def click_blue_button(self):
        self.set_series_visibility(False, False, False, True)

    # 更新需要调整的图像
    def set_pixmap(self, pixmap: QPixmap):
        self.pixmap = pixmap
