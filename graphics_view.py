from PyQt5.QtCore import QRectF, Qt, pyqtSignal
from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QGraphicsItem

from crop_box import CropBox


class GraphicsView(QGraphicsView):
    save_signal = pyqtSignal(bool)  # 保存图片信号
    scale_signal = pyqtSignal(float)  # 图片缩放信号

    def __init__(self, pixmap, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.setTransformationAnchor(QGraphicsView.NoAnchor)  # 设置缩放或旋转基于视图中心调整
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)  # 设置视图放大缩小时基于鼠标点调整


        # 设置scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # 设置图元
        self.pixmap_item = GraphicsPixmapItem(pixmap)  # 设置图元内图像
        self.pixmap_item.setFlag(QGraphicsItem.ItemIsSelectable)  # 设置允许选中图元
        self.scene.addItem(self.pixmap_item)  # 添加图元到场景
        self.min_ratio = None  # 最小缩放倍数（根据图片大小动态设置）
        self.MAX_RATIO = 50.00  # 最大缩放倍数5000倍
        self.cur_scale_ratio = None  # 当前缩放倍数
        self.ZOOM_IN_FACTOR = 1.1  # 放大比例
        self.ZOOM_OUT_FACTOR = 0.9  # 缩小比例

        # 调整图片以合适的大小显示
        self.zoom_fitted_view()

        self.crop_box = None  # 初始化裁剪框

    def add_crop_box(self):
        try:
            self.crop_box = CropBox(parent=self.pixmap_item)
            self.scene.addItem(self.crop_box)
        except Exception as e:
            print("Error:", e)

    def delete_crop_box(self):
        try:
            if self.crop_box is not None:
                self.scene.removeItem(self.crop_box)
                self.crop_box = None
        except Exception as e:
            print("Error:", e)

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

        TARGET_RATIO = 2 / 5  # 缩放目标比例为窗口的2/5
        # 计算缩放比例，根据不同情况缩小视图
        if x_ratio > TARGET_RATIO or y_ratio > TARGET_RATIO:
            scale_ratio = TARGET_RATIO / max(x_ratio, y_ratio)
        else:
            scale_ratio = 1.0  # 不需要缩放
        self.scale(scale_ratio, scale_ratio)
        self.min_ratio = round(scale_ratio, 2)  # 保留2位小数
        self.cur_scale_ratio = round(scale_ratio, 2)
        print("image scale:", self.cur_scale_ratio)


class GraphicsPixmapItem(QGraphicsPixmapItem):
    save_signal = pyqtSignal(bool)

    def __init__(self, image):
        super().__init__()
        self.setPixmap(image)  # 设置图元内图像
        self.setAcceptHoverEvents(True)  # 开启接受伪状态事件
        self.current_point = None  # 鼠标当前坐标
        self.start_point = None  # 鼠标点击时的坐标

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        self.current_point = event.pos()
        print(self.pos().x(), self.pos().y())
        self.moveBy(self.current_point.x() - self.start_point.x(),
                    self.current_point.y() - self.start_point.y())


    # 鼠标按压事件
    def mousePressEvent(self, event):
        super(GraphicsPixmapItem, self).mousePressEvent(event)

        self.start_point = event.pos()

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)

    # 伪状态移动事件设置鼠标样式
    def hoverMoveEvent(self, event):
        try:
            if QRectF(self.pixmap().rect()).contains(event.pos()):
                self.setCursor(Qt.OpenHandCursor)
        except Exception as e:
            print("Error:", e)

