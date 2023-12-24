from PyQt5.QtCore import pyqtSignal, QRect
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

from crop_box import CropBox
from graphics_pixmap import GraphicsPixmapItem
from tools.text import Text


class GraphicsView(QGraphicsView):
    save_signal = pyqtSignal(bool)  # 保存图片信号
    scale_signal = pyqtSignal(float)  # 图片缩放信号

    def __init__(self, pixmap, parent=None):
        super(GraphicsView, self).__init__(parent)
        # self.setTransformationAnchor(QGraphicsView.NoAnchor)  # 设置缩放或旋转基于视图中心调整
        # self.setResizeAnchor(QGraphicsView.AnchorViewCenter)  # 设置视图放大缩小时基于鼠标点调整

        # 设置scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # 设置图元
        self.pixmap_item = GraphicsPixmapItem(pixmap)  # 设置图元内图像
        self.scene.addItem(self.pixmap_item)  # 添加图元到场景
        self.min_ratio = 0.1  # 最小缩放倍数（根据图片大小动态设置）
        self.MAX_RATIO = 50.00  # 最大缩放倍数5000倍
        self.cur_scale_ratio = None  # 当前缩放倍数
        self.ZOOM_IN_FACTOR = 1.1  # 放大比例
        self.ZOOM_OUT_FACTOR = 0.9  # 缩小比例

        # 调整图片以合适的大小显示
        self.zoom_fitted_view()

        self.crop_box = None  # 初始化裁剪框

        self.text_stack = []  # 文本类的栈

    # 添加裁剪框
    def add_crop_box(self):
        try:
            self.crop_box = CropBox(parent=self.pixmap_item)
            self.scene.addItem(self.crop_box)
        except Exception as e:
            print("Error:", e)

    # 隐藏裁剪框
    def hide_crop_box(self):
        try:
            if self.crop_box:
                self.crop_box.hide()
        except Exception as e:
            print("Error:", e)

    # 显示裁剪框
    def show_crop_box(self):
        try:
            if self.crop_box:
                self.crop_box.show()
                self.crop_box.update_pos()
        except Exception as e:
            print("Error:", e)

    # 添加文本编辑框
    def add_text_edit(self):
        try:
            text = Text(parent=self.pixmap_item)
            self.text_stack.append(text)  # 添加到文本类栈
            self.scene.addItem(text)  # 添加到场景
        except Exception as e:
            print("Error:", e)

    # 绘制文本到图像
    def draw_text(self):
        pixmap = self.get_pixmap()
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿
        # 设置裁剪区域为图像大小
        clip_rect = QRect(0, 0, pixmap.width(), pixmap.height())
        painter.setClipRect(clip_rect)
        for text in self.text_stack:
            rect = text.parent_rect()  # 获取文本矩形位置
            painter.setPen(text.defaultTextColor())  # 设置笔颜色
            painter.setFont(text.font())  # 设置字体
            painter.drawText(rect, text.toPlainText())  # 绘制文本
        painter.end()  # 结束 QPainter 操作
        self.set_pixmap(pixmap)  # 更新添加文字后的图像

    # 删除所有文本
    def delete_text(self):
        try:
            for text in self.text_stack:
                self.scene.removeItem(text)
            self.text_stack.clear()
        except Exception as e:
            print("Error:", e)

    # 获取当前的文本类
    def get_text(self):
        # 遍历栈查找是否有文本类被选中
        for text in self.text_stack:
            if text.isSelected():
                return text
        # 没有被选中的则返回栈顶文本
        if len(self.text_stack) != 0:
            return self.text_stack[-1]
        else:
            return False

    # 改变文本类颜色
    def change_text_color(self, color: QColor):
        if self.get_text():
            text = self.get_text()
            text.setDefaultTextColor(color)

    # 改变文本类字体
    def change_text_font(self, font: QFont):
        if self.get_text():
            text = self.get_text()
            text.setFont(font)

    # 使用SpinBox调整字体大小
    def spinbox_change(self, font_size):
        if self.get_text():
            text = self.get_text()
            font = text.font()
            font.setPointSize(font_size)
            text.setFont(font)

    # 滚轮事件
    def wheelEvent(self, event):
        # 滚轮前滚放大
        if event.angleDelta().y() > 0:
            # 放大不能超过最大倍数
            if self.cur_scale_ratio * self.ZOOM_IN_FACTOR < self.MAX_RATIO:
                zoom_factor = self.ZOOM_IN_FACTOR
                self.cur_scale_ratio *= self.ZOOM_IN_FACTOR
            else:
                zoom_factor = self.MAX_RATIO / self.cur_scale_ratio
                self.cur_scale_ratio = self.MAX_RATIO
        # 滚轮后滚缩小
        else:
            # 缩小不能小于最小倍数
            if self.cur_scale_ratio * self.ZOOM_OUT_FACTOR > self.min_ratio:
                zoom_factor = self.ZOOM_OUT_FACTOR
                self.cur_scale_ratio *= self.ZOOM_OUT_FACTOR
            else:
                zoom_factor = self.min_ratio / self.cur_scale_ratio
                self.cur_scale_ratio = self.min_ratio
        self.scale(zoom_factor, zoom_factor)  # 根据缩放比例进行缩放
        self.scale_signal.emit(self.cur_scale_ratio)  # 发射图片缩放信号

    # 放大视图
    def zoom_in_view(self):
        # 放大不能超过最大倍数
        if self.cur_scale_ratio * self.ZOOM_IN_FACTOR < self.MAX_RATIO:
            zoom_factor = self.ZOOM_IN_FACTOR
            self.cur_scale_ratio *= self.ZOOM_IN_FACTOR
        else:
            zoom_factor = self.MAX_RATIO / self.cur_scale_ratio
            self.cur_scale_ratio = self.MAX_RATIO
        self.scale(zoom_factor, zoom_factor)  # 根据缩放比例进行缩放
        self.scale_signal.emit(self.cur_scale_ratio)  # 发射图片缩放信号

    # 缩小视图
    def zoom_out_view(self):
        # 缩小不能小于最小倍数
        if self.cur_scale_ratio * self.ZOOM_OUT_FACTOR > self.min_ratio:
            zoom_factor = self.ZOOM_OUT_FACTOR
            self.cur_scale_ratio *= self.ZOOM_OUT_FACTOR
        else:
            zoom_factor = self.min_ratio / self.cur_scale_ratio
            self.cur_scale_ratio = self.min_ratio
        self.scale(zoom_factor, zoom_factor)  # 根据缩放比例进行缩放
        self.scale_signal.emit(self.cur_scale_ratio)  # 发射图片缩放信号

    # # 鼠标释放事件
    # def mouseReleaseEvent(self, event):
    #     pass

    # 缩放视图到合适比例
    def zoom_fitted_view(self):
        parent_widget_size = self.parentWidget().size()
        pixmap_size = self.pixmap_item.pixmap().size()
        x_ratio = pixmap_size.width() / parent_widget_size.width()
        y_ratio = pixmap_size.height() / parent_widget_size.height()

        target_ratio = 2 / 5  # 缩放目标比例为窗口的2/5
        # 计算缩放比例，根据不同情况缩小视图
        if x_ratio > target_ratio or y_ratio > target_ratio:
            scale_ratio = target_ratio / max(x_ratio, y_ratio)
        else:
            scale_ratio = 1.0  # 不需要缩放
        self.scale(scale_ratio, scale_ratio)
        # self.min_ratio = round(scale_ratio, 2)  # 保留2位小数
        self.cur_scale_ratio = round(scale_ratio, 2)
        print("image scale:", self.cur_scale_ratio)

    # 获取pixmap
    def get_pixmap(self):
        return self.pixmap_item.pixmap()

    # 设置pixmap
    def set_pixmap(self, pixmap: QPixmap):
        self.pixmap_item.setPixmap(pixmap)
