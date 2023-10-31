from PyQt5.QtCore import QRectF, Qt, pyqtSignal, QRect, QPointF, QSizeF
from PyQt5.QtGui import QColor, QPixmap, QPen, QPainterPath, QPainter, QTransform
from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QGraphicsItem

from crop_box import CropBox


class GraphicsView(QGraphicsView):
    save_signal = pyqtSignal(bool)  # 保存图片信号
    scale_signal = pyqtSignal(float)  # 图片缩放信号

    def __init__(self, pixmap, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.setTransformationAnchor(QGraphicsView.NoAnchor)  # 设置缩放或旋转基于视图中心调整
        # self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)  # 设置视图放大缩小时基于鼠标点调整

        # 设置scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        # 设置图元
        self.pixmap_item = GraphicsPixmapItem(pixmap)  # 设置图元内图像
        self.pixmap_item.setFlag(QGraphicsItem.ItemIsMovable)  # 设置允许拖动图元改变位置
        self.scene.addItem(self.pixmap_item)  # 添加图元到场景
        self.min_ratio = None  # 最小缩放倍数（根据图片大小动态设置）
        self.max_ratio = 50.00  # 最大缩放倍数5000倍
        self.cur_scale_ratio = None  # 当前缩放倍数

        self.pixmap_item.setPos(0, 0)
        # size = self.image_item.pixmap().size()
        # 调整图片以合适的大小显示
        self.zoom_fitted_view()
        # self.image_item.setPos(size.width() / 2, size.height() / 2)
        # self.scale(0.1, 0.1)

        # self.add_new_crop_box()

    def add_crop_box(self):
        try:
            self.scene.addItem(
                CropBox(
                    size=self.pixmap_item.pixmap().rect().size(),
                    limit_rect=QRectF(self.pixmap_item.pixmap().rect()),
                    parent=self.pixmap_item
                )
            )
        except Exception as e:
            print("Error:", e)

    # def resizeEvent(self, event):
    #     super().resizeEvent(event)  # 调用父类的resizeEvent方法
    #     print("resize event")
    #     self.zoom_fitted_view()

    # 滚轮事件
    def wheelEvent(self, event):
        zoom_in_factor = 1.1  # 放大比例
        zoom_out_factor = 0.9  # 缩小比例
        # 滚轮前滚放大
        if event.angleDelta().y() > 0:
            # 放大不能超过最大倍数
            if self.cur_scale_ratio * zoom_in_factor < self.max_ratio:
                zoom_factor = zoom_in_factor
                self.cur_scale_ratio *= zoom_in_factor
            else:
                zoom_factor = self.max_ratio / self.cur_scale_ratio
                self.cur_scale_ratio = self.max_ratio
        # 滚轮后滚缩小
        else:
            # 缩小不能小于最小倍数
            if self.cur_scale_ratio * zoom_out_factor > self.min_ratio:
                zoom_factor = zoom_out_factor
                self.cur_scale_ratio *= zoom_out_factor
            else:
                zoom_factor = self.min_ratio / self.cur_scale_ratio
                self.cur_scale_ratio = self.min_ratio
        self.scale(zoom_factor, zoom_factor)
        print(self.cur_scale_ratio)
        self.scale_signal.emit(self.cur_scale_ratio)  # 发射图片缩放信号

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        # print(self.image_item.is_finish_cut, self.image_item.is_start_cut)
        if self.pixmap_item.is_finish_cut:
            self.save_signal.emit(True)
        else:
            self.save_signal.emit(False)

    # 缩放视图到合适比例
    def zoom_fitted_view(self):
        parent_widget_size = self.parentWidget().size()
        pixmap_size = self.pixmap_item.pixmap().size()
        x_ratio = pixmap_size.width() / parent_widget_size.width()
        y_ratio = pixmap_size.height() / parent_widget_size.height()

        TARGET_RATIO = 2 / 5  # 缩放目标比例
        # 计算缩放比例，根据不同情况缩小视图
        if x_ratio > TARGET_RATIO or y_ratio > TARGET_RATIO:
            scale_ratio = TARGET_RATIO / max(x_ratio, y_ratio)
        else:
            scale_ratio = 1.0  # 不需要缩放
        self.scale(scale_ratio, scale_ratio)
        self.min_ratio = round(scale_ratio, 2)  # 保留2位小数
        self.cur_scale_ratio = round(scale_ratio, 2)
        self.scale_signal.emit(self.cur_scale_ratio)  # 发射图片缩放信号
        print("image scale:", self.cur_scale_ratio)


class GraphicsPixmapItem(QGraphicsPixmapItem):
    save_signal = pyqtSignal(bool)

    def __init__(self, image):
        super().__init__()
        self.setPixmap(image)  # 设置图元内图像
        self.setAcceptHoverEvents(True)  # 开启接受伪状态事件
        self.is_start_cut = False  # 开始裁剪
        self.current_point = None
        self.start_point = None
        self.is_finish_cut = False
        # print(self.pixmap().size())

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        self.current_point = event.pos()
        # if not self.is_start_cut:
        #     # self.setCursor(Qt.ClosedHandCursor)
        self.moveBy(self.current_point.x() - self.start_point.x(),
                    self.current_point.y() - self.start_point.y())
        # 移动图元时更新裁剪框位置和状态
        # for item in self.scene().items():
        #     if isinstance(item, CropBox):
        #         try:
        #             # 重新设置裁剪框大小和位置
        #             box_point = QPointF(self.pos())
        #             box_size = QSizeF(item.getWidth(), item.getHeight())
        #             item.setState(box_point, box_size)
        #             # 重新设置裁剪框限制大小的矩形位置
        #             limit_box = QRectF(self.pixmap().rect())
        #             item.setLimit(self.mapRectToScene(limit_box))
        #         except Exception as e:
        #             print("Error:", e)
        # self.is_finish_cut = False
        self.update()

    # 鼠标按压事件
    def mousePressEvent(self, event):
        super(GraphicsPixmapItem, self).mousePressEvent(event)
        # self.setCursor(Qt.OpenHandCursor)
        self.start_point = event.pos()
        self.current_point = None
        self.is_finish_cut = False
        if event.button() == Qt.MidButton:
            self.is_midbutton = True
            self.update()
        else:
            self.is_midbutton = False
            self.update()

    # def mouseReleaseEvent(self, event):
    #     self.setCursor(Qt.OpenHandCursor)

    # 伪状态移动事件设置鼠标样式
    def hoverMoveEvent(self, event):
        try:
            if QRectF(self.pixmap().rect()).contains(event.pos()):
                self.setCursor(Qt.OpenHandCursor)
        except Exception as e:
            print("Error:", e)

    # def paint(self, painter, option, widget):
    #     try:
    #         print("paint from GraphicsPixmapItem")
    #         super(GraphicsPixmapItem, self).paint(painter, option, widget)
    #         if self.is_start_cut:
    #             border_path = QPainterPath()
    #             crop_box_path = QPainterPath()
    #             # 获取GraphicsPixmapItem整体区域
    #             border_path.setFillRule(Qt.WindingFill)
    #             # border路径的填充规则为奇偶规则，奇次填充偶次不填充
    #             crop_box_path.setFillRule(Qt.WindingFill)
    #             border_path.addRect(self.boundingRect())  # 添加一个矩形，boundingRect()返回当前图形项的边界矩形
    #             # 添加裁剪框矩形形状
    #             crop_box_path.addRect(
    #                 self.crop_box.pos().x() + 2,
    #                 self.crop_box.pos().y() + 2,
    #                 self.crop_box.width() - 4,
    #                 self.crop_box.height() - 4
    #             )
    #             # 2者相减，得到裁切框外部的区域
    #             end_path = border_path.subtracted(crop_box_path)
    #             # 使用画笔，对这个区域简单加一层有一定透明度的遮罩
    #             painter.setRenderHint(QPainter.Antialiasing, True)  # 启用抗锯齿
    #             painter.fillPath(end_path, QColor(0, 0, 0, 100))
    #
    #             # print(self.start_point, self.current_point)
    #             # pen = QPen(Qt.DashLine)
    #             # pen.setColor(QColor(0, 150, 0, 70))
    #             # pen.setWidth(3)
    #             # painter.setPen(pen)
    #             # painter.setBrush(QColor(255, 255, 255, 70))
    #             # if not self.current_point:
    #             #     return
    #             # painter.drawRect(QRectF(self.start_point, self.current_point))
    #             # self.end_point = self.current_point
    #             # self.is_finish_cut = True
    #     except Exception as e:
    #         print("Error:", e)
