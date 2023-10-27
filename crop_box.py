import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QSizeF, QSize, QRectF, QPointF
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor
from PyQt5.Qt import QTextOption, QPoint, QRect


# 裁剪框类
class CropBox(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # self.min_width = 80  # 最小宽度
        # self.min_height = 80  # 最小高度
        self.left_button_clicked = False  # 裁剪框被鼠标左键点击标志
        # self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)  # 透明背景
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏系统边框
        self.setMouseTracking(True)  # 开启鼠标追踪

        # 定义窗口的八个边界范围，用来调整窗口大小
        self._top_rect = None  # 顶部
        self._bottom_rect = None  # 底部
        self._left_rect = None  # 左侧
        self._right_rect = None  # 右侧
        self._left_top_rect = None  # 左上角
        self._right_top_rect = None  # 右上角
        self._left_bottom_rect = None  # 左下角
        self._right_bottom_rect = None  # 右下角

        # 设置八个方向的鼠标拖拽放缩判断扳机默认值
        self._top_drag = False
        self._bottom_drag = False
        self._left_drag = False
        self._right_drag = False
        self._left_top_drag = False
        self._right_top_drag = False
        self._left_bottom_drag = False
        self._right_bottom_drag = False
        self._move_drag = False  # 鼠标拖拽移动扳机
        self.move_DragPosition = None  # 裁剪框拖拽坐标

        self._padding = 8  # widget可拖拽调整大小区域宽度8px

    # 绘制事件
    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            self.draw_internal_lines(painter)  # 绘制裁剪框内部虚线
            self.draw_border(painter)  # 绘制裁剪框边框实线
            # self.draw_border_points(painter)  # 绘制边框上八个方向的顶点
            # self.draw_size_text(painter)  # 绘制当前裁剪框像素大小文本
        except Exception as e:
            print("Error:paintEvent", e)

    def resizeEvent(self, event):
        # 重新调整边界范围以备实现鼠标拖放缩放窗口大小，采用八个列表生成式生成八个坐标范围
        self._left_rect = [QPoint(x, y) for x in range(1, self._padding + 1)
                           for y in range(self._padding + 1, self.height() - self._padding)]
        self._right_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                            for y in range(self._padding + 1, self.height() - self._padding)]
        self._top_rect = [QPoint(x, y) for x in range(self._padding + 1, self.width() - self._padding)
                          for y in range(1, self._padding + 1)]
        self._bottom_rect = [QPoint(x, y) for x in range(self._padding + 1, self.width() - self._padding)
                             for y in range(self.height() - self._padding, self.height() + 1)]
        self._right_bottom_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                                   for y in range(self.height() - self._padding, self.height() + 1)]
        self._left_bottom_rect = [QPoint(x, y) for x in range(1, self._padding + 1)
                                  for y in range(self.height() - self._padding, self.height() + 1)]
        self._right_top_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                                for y in range(1, self._padding + 1)]
        self._left_top_rect = [QPoint(x, y) for x in range(1, self._padding + 1)
                               for y in range(1, self._padding + 1)]

    # 重写鼠标点击事件
    def mousePressEvent(self, event):
        # 鼠标左键按下
        if event.button() == Qt.LeftButton:
            self.left_button_clicked = True  # 开启鼠标左键点击标志
            if event.pos() in self._top_rect:
                # 鼠标左键点击上侧边界区域
                self._top_drag = True
                event.accept()
            elif event.pos() in self._bottom_rect:
                # 鼠标左键点击下侧边界区域
                self._bottom_drag = True
                event.accept()
            elif event.pos() in self._left_rect:
                # 鼠标左键点击左侧边界区域
                self._left_drag = True
                event.accept()
            elif event.pos() in self._right_rect:
                # 鼠标左键点击右侧边界区域
                self._right_drag = True
                event.accept()
            elif event.pos() in self._left_top_rect:
                # 鼠标左键点击左上角边界区域
                self._left_top_drag = True
                event.accept()
            elif event.pos() in self._right_bottom_rect:
                # 鼠标左键点击右下角边界区域
                self._right_bottom_drag = True
                event.accept()
            elif event.pos() in self._right_top_rect:
                # 鼠标左键点击右上角边界区域
                self._right_top_drag = True
                event.accept()
            elif event.pos() in self._left_bottom_rect:
                # 鼠标左键点击左下角边界区域
                self._left_bottom_drag = True
                event.accept()
            else:
                # 鼠标点击中间区域，进行移动
                self._move_drag = True  # 开启移动拖拽标志
                # 鼠标点击时的全局坐标 - 裁切框的左上角坐标 = 裁剪框的初始拖拽坐标
                self.move_DragPosition = event.globalPos() - self.pos()
                self.setCursor(Qt.ClosedHandCursor)
                event.accept()

    # 重写鼠标释放事件
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.cursor() == Qt.ClosedHandCursor:
                self.setCursor(Qt.OpenHandCursor)
            # 鼠标释放后各扳机复位
            self.left_button_clicked = False  # 关闭裁剪框被点击标志

            self._top_drag = False
            self._bottom_drag = False
            self._left_drag = False
            self._right_drag = False
            self._left_top_drag = False
            self._right_top_drag = False
            self._left_bottom_drag = False
            self._right_bottom_drag = False

            self._move_drag = False
        event.accept()

    # 重写鼠标移动事件
    def mouseMoveEvent(self, event):
        point = event.pos()  # 获取鼠标相对于裁切框的坐标
        parent_point = self.mapToParent(point)  # 将鼠标事件的局部坐标映射到父级坐标系中的坐标
        # 鼠标没点击时，根据光标位置设置光标样式
        if not self.left_button_clicked:
            self._set_cursor(event.pos())
        # 调整窗口大小
        if Qt.LeftButton:
            if self._left_drag:
                # 左侧调整窗口宽度
                new_width = self.width() + (self.x() - event.globalPos().x())
                if new_width >= self.minimumWidth():
                    self.setGeometry(event.globalPos().x(), self.y(), new_width, self.height())
                event.accept()
            elif self._top_drag:
                # 顶部调整窗口高度
                new_height = self.height() + (self.y() - event.globalPos().y())
                if new_height >= self.minimumHeight():
                    self.setGeometry(self.x(), event.globalPos().y(), self.width(), new_height)
                event.accept()
            elif self._left_top_drag:
                # 左上角调整窗口大小
                new_width = self.width() + (self.x() - event.globalPos().x())
                new_height = self.height() + (self.y() - event.globalPos().y())
                if new_width >= self.minimumWidth() and new_height >= self.minimumHeight():
                    self.setGeometry(event.globalPos().x(), event.globalPos().y(), new_width, new_height)
                event.accept()
            elif self._right_top_drag:
                # 右上角调整窗口大小
                new_width = event.globalPos().x() - self.x()
                new_height = self.height() + (self.y() - event.globalPos().y())
                if new_width >= self.minimumWidth() and new_height >= self.minimumHeight():
                    self.setGeometry(self.x(), event.globalPos().y(), new_width, new_height)
                event.accept()
            elif self._left_bottom_drag:
                # 左下角调整窗口大小
                new_width = self.width() + (self.x() - event.globalPos().x())
                new_height = event.globalPos().y() - self.y()
                if new_width >= self.minimumWidth() and new_height >= self.minimumHeight():
                    self.setGeometry(event.globalPos().x(), self.y(), new_width, new_height)
                event.accept()
            # 仅对于右下的方向，可以用resize实现，更平滑
            elif self._right_drag:
                # 右侧调整窗口宽度
                self.resize(event.pos().x(), self.height())
                event.accept()
            elif self._bottom_drag:
                # 底部调整窗口高度
                self.resize(self.width(), event.pos().y())
                event.accept()
            elif self._right_bottom_drag:
                # 右下角同时调整高度和宽度
                self.resize(event.pos().x(), event.pos().y())
                event.accept()
            elif self._move_drag:
                # 拖动窗口
                self.move(event.globalPos() - self.move_DragPosition)
                event.accept()

    # 根据光标位置设置光标样式
    def _set_cursor(self, point):
        if point in self._left_rect:
            # 左侧边界
            self.setCursor(Qt.SizeHorCursor)
        elif point in self._right_rect:
            # 右侧边界
            self.setCursor(Qt.SizeHorCursor)
        elif point in self._bottom_rect:
            # 底下边界
            self.setCursor(Qt.SizeVerCursor)
        elif point in self._top_rect:
            # 顶部边界
            self.setCursor(Qt.SizeVerCursor)
        elif point in self._left_top_rect:
            # 左上角边界
            self.setCursor(Qt.SizeFDiagCursor)
        elif point in self._left_bottom_rect:
            # 左下角边界
            self.setCursor(Qt.SizeBDiagCursor)
        elif point in self._right_top_rect:
            # 右上角边界
            self.setCursor(Qt.SizeBDiagCursor)
        elif point in self._right_bottom_rect:
            # 右下角边界
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            self.setCursor(Qt.OpenHandCursor)

    # 绘制裁剪框边框实线
    def draw_border(self, painter):
        try:
            pen = QPen(QColor(3, 125, 203), 5)  # 笔线宽5个像素
            painter.setPen(pen)
            painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
        except Exception as e:
            print("Error: draw_border", e)

    # 绘制边框上八个方向的顶点
    def draw_border_points(self, painter):
        pen = QPen(QColor(3, 125, 203), 5)  # 笔线宽5个像素
        painter.setPen(pen)
        painter.drawPoint(2, 2)  # 左上角
        painter.drawPoint(self.width() // 2, 2)  # 顶部
        painter.drawPoint(self.width() - 2, 2)  # 右上角
        painter.drawPoint(2, self.height() // 2)  # 左侧
        painter.drawPoint(2, self.height() - 2)  # 左下角
        painter.drawPoint(self.width() - 2, self.height() // 2)  # 右侧
        painter.drawPoint(self.width() - 2, self.height() - 2)  # 右下角
        painter.drawPoint(self.width() // 2, self.height() - 2)  # 底部

    # 绘制裁剪框内部虚线
    def draw_internal_lines(self, painter):
        crop_box_path = QPainterPath()  # 绘图区域
        crop_box_path.addRect(2, 2, self.width() - 4, self.height() - 4)  # 添加矩形区域
        painter.setClipPath(crop_box_path)  # 设置被限制的绘画区域为crop_box_path
        painter.setClipping(True)  # 启用剪切限制
        # 绘画内部虚线线条
        pen = QPen(QColor(230, 230, 230), 1, Qt.DashLine)  # 笔线宽1，为虚线
        painter.setPen(pen)
        # 绘制2条垂直虚线
        for i in range(1, 3):
            width = self.width() // 3
            painter.drawLine(i * width, 2, i * width, self.height() - 2)
        # 绘制2条水平虚线
        for i in range(1, 3):
            height = self.height() // 3
            painter.drawLine(2, i * height, self.width() - 2, i * height)
        # 绘画完，取消被限制的区域
        painter.setClipping(False)

    # 绘制当前裁剪框像素大小文本
    def draw_size_text(self, painter):
        # 通过在裁剪框底部开辟一块矩形区来实现
        pen = QPen(QColor(255, 0, 0))  # 红笔
        painter.setPen(pen)
        size_text = f"({self.width()}, {self.height()})"  # 使用f-string格式化字符串
        top_left = QPointF(self.width() - self.min_width, self.height() - 20)  # 文本绘制区域的左上角坐标
        size = QSizeF(self.min_width, 20)
        rect = QRectF(top_left, size)
        option = QTextOption()  # 文本垂直方向居中对齐，水平方向右对齐
        painter.drawText(rect, size_text, option)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_win = CropBox(None)
    app_win.show()
    sys.exit(app.exec_())
