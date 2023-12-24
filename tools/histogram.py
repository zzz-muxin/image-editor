import cv2
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor

from tools.image_format import ImageFormat


# 灰度直方图图表类
class GrayChart(QChartView):
    def __init__(self, pixmap: QPixmap):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿

        self.pixmap = pixmap  # 原始图像
        self.gray_hist = None  # 初始化灰度直方图
        self.line_series = QLineSeries()  # 折线系列
        self.chart = QChart()  # 图表
        self.axis_x = QValueAxis()  # x轴
        self.axis_y = QValueAxis()  # y轴

        # 必须先插入系列数据再处理图表的轴，否则不会有轴
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
        self.chart.legend().hide()  # 隐藏图例
        # self.chart.legend().setVisible(True)  # 设置图例可见
        # self.chart.setTheme(QChart.ChartThemeDark)  # 表格主题颜色
        self.chart.setAnimationOptions(QChart.SeriesAnimations)  # 启用系列动画

        self.axis_x.setLabelFormat("%d")  # x轴使用整数格式显示刻度标签
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)  # 添加x轴到chart底部
        self.line_series.attachAxis(self.axis_x)  # 关联折线

        self.axis_y.setLabelFormat("%d")  # y轴使用整数格式显示刻度标签
        self.axis_y.setRange(0, max(self.gray_hist)[0])  # y轴限制显示范围
        print(min(self.gray_hist)[0], max(self.gray_hist)[0])
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)  # 添加y轴到chart左部
        self.line_series.attachAxis(self.axis_y)  # 关联折线

    # 初始化折线数据
    def init_series(self):
        # 添加直方图数据到表格
        for i in range(256):
            self.line_series.append(i, self.gray_hist[i][0])

    # 更新直方图
    def update_chart(self):
        self.calculate_histogram()
        # 更新折线系列的数据
        for i in range(256):
            self.line_series.replace(i, i, self.gray_hist[i][0])
        # 强制图表刷新
        self.axis_y.setRange(0, max(self.gray_hist)[0])  # y轴限制显示范围
        self.chart.update()

    def set_pixmap(self, pixmap):
        self.pixmap = pixmap
        self.update_chart()


# rgb直方图图表类
class RGBChart(QChartView):
    image_updated = pyqtSignal(QPixmap)  # 图片更新信号

    def __init__(self, pixmap: QPixmap):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿

        self.pixmap = pixmap  # 原始图像
        # 初始化rgb直方图
        self.red_hist = None
        self.green_hist = None
        self.blue_hist = None
        # 均衡化后的直方图
        self.red_hist_equalize = None
        self.green_hist_equalize = None
        self.blue_hist_equalize = None
        self.line_series_r = QLineSeries()  # r折线系列
        self.line_series_g = QLineSeries()  # g折线系列
        self.line_series_b = QLineSeries()  # b折线系列
        self.chart = QChart()  # 图表
        self.axis_x = QValueAxis()  # x轴
        self.axis_y = QValueAxis()  # y轴

        # 必须先插入数据再处理图表的轴，否则不会有轴
        self.init_series()
        self.init_chart()

        self.setChart(self.chart)  # 设置QChartView的chart

    # 初始化图表
    def init_chart(self):
        # 添加rgb通道折线系列
        self.chart.addSeries(self.line_series_r)
        self.chart.addSeries(self.line_series_g)
        self.chart.addSeries(self.line_series_b)
        self.chart.setTitle("RGB Histogram")  # 表格标题
        self.chart.legend().hide()  # 隐藏图例
        self.chart.legend().setAlignment(Qt.AlignBottom)  # 设置图例在表格底部
        # self.chart.setTheme(QChart.ChartThemeDark)  # 表格主题颜色
        self.chart.setAnimationOptions(QChart.SeriesAnimations)  # 启用系列动画

        self.axis_x.setLabelFormat("%d")  # x轴使用整数格式显示刻度标签
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)  # 添加x轴到chart底部
        # x轴关联rgb折线
        self.line_series_r.attachAxis(self.axis_x)
        self.line_series_g.attachAxis(self.axis_x)
        self.line_series_b.attachAxis(self.axis_x)

        self.axis_y.setLabelFormat("%d")  # y轴使用整数格式显示刻度标签
        # 计算三个通道出现的最大频率，设置y轴的显示范围
        red_max_value = max(self.red_hist)[0]
        green_max_value = max(self.green_hist)[0]
        blue_max_value = max(self.blue_hist)[0]
        max_value = max(red_max_value, green_max_value, blue_max_value)
        self.axis_y.setRange(0, max_value)  # y轴限制显示范围
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)  # 添加y轴到chart左部
        # y轴关联rgb折线
        self.line_series_r.attachAxis(self.axis_y)
        self.line_series_g.attachAxis(self.axis_y)
        self.line_series_b.attachAxis(self.axis_y)

    # 初始化折线序列
    def init_series(self):
        # 计算直方图数据
        self.red_hist, self.green_hist, self.blue_hist = self.calculate_histogram(self.pixmap)
        # 设置rgb折线颜色
        self.line_series_r.setColor(QColor(240, 0, 0))
        self.line_series_g.setColor(QColor(33, 255, 53))
        self.line_series_b.setColor(QColor(2, 132, 252))
        # 设置折线图例文本
        self.line_series_r.setName("Red")
        self.line_series_g.setName("Green")
        self.line_series_b.setName("Blue")
        # 添加直方图数据
        for i in range(256):
            self.line_series_r.append(i, self.red_hist[i][0])
            self.line_series_g.append(i, self.green_hist[i][0])
            self.line_series_b.append(i, self.blue_hist[i][0])

    # 计算直方图
    @staticmethod
    def calculate_histogram(pixmap):
        cv_image = ImageFormat.pixmap_to_cv(pixmap)  # 转换为cv图像
        # 分别计算三个通道的直方图
        red_hist = cv2.calcHist([cv_image], [2], None, [256], [0, 256])
        green_hist = cv2.calcHist([cv_image], [1], None, [256], [0, 256])
        blue_hist = cv2.calcHist([cv_image], [0], None, [256], [0, 256])
        return red_hist, green_hist, blue_hist

    # 更新图表
    def update_chart(self, pixmap):
        red_hist, green_hist, blue_hist = self.calculate_histogram(pixmap)
        # 更新折线系列的数据
        for i in range(256):
            self.line_series_r.replace(i, i, red_hist[i][0])
            self.line_series_g.replace(i, i, green_hist[i][0])
            self.line_series_b.replace(i, i, blue_hist[i][0])
        # 计算三个通道出现的最大频率，设置y轴的显示范围
        red_max_value = max(red_hist)[0]
        green_max_value = max(green_hist)[0]
        blue_max_value = max(blue_hist)[0]
        max_value = max(red_max_value, green_max_value, blue_max_value)
        self.axis_y.setRange(0, max_value)  # y轴限制显示范围
        # 强制图表刷新
        self.chart.update()

    # rgb直方图均衡化
    def hist_equalize(self):
        cv_image = ImageFormat.pixmap_to_cv(self.pixmap)  # 转换为cv图像
        b, g, r, a = cv2.split(cv_image)  # 通道分解
        # 分别计算三个通道的均衡化直方图
        self.red_hist_equalize = cv2.equalizeHist(r)
        self.green_hist_equalize = cv2.equalizeHist(g)
        self.blue_hist_equalize = cv2.equalizeHist(b)
        # 通道合并
        result = cv2.merge((self.blue_hist_equalize, self.green_hist_equalize, self.red_hist_equalize, a))
        new_pixmap = ImageFormat.cv_to_pixmap(result)
        self.update_chart(new_pixmap)
        self.image_updated.emit(new_pixmap)  # 发射图片更新信号

    # 恢复原直方图
    def hist_restore(self):
        self.update_chart(self.pixmap)
        self.image_updated.emit(self.pixmap)  # 发射图片更新信号

    def set_pixmap(self, pixmap):
        self.pixmap = pixmap
        self.update_chart(pixmap)
