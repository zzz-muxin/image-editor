from PyQt5.QtCore import QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPixmap, QPen, QPainterPath, QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QGraphicsItem


class GraphicsView(QGraphicsView):
    save_signal = pyqtSignal(bool)  # 保存图片信号

    def __init__(self, image, parent=None):
        super(GraphicsView, self).__init__(parent)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)  # 设置缩放或旋转基于鼠标点调整
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)  # 设置视图放大缩小时基于鼠标点调整

        # 设置scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        # 设置图元
        self.image_item = GraphicsPixmapItem(QPixmap(image))  # 设置图元内图像
        self.image_item.setFlag(QGraphicsItem.ItemIsMovable)  # 设置允许拖动图元改变位置
        self.scene.addItem(self.image_item)  # 添加图元到场景

        size = self.image_item.pixmap().size()
        # 调整图片在中间
        self.image_item.setPos(size.width() / 2, size.height() / 2)
        self.scale(0.1, 0.1)
    # 滚轮事件
    def wheelEvent(self, event):
        print("wheelEvent from GraphicsView")
        zoomInFactor = 1.25  # 放大比例
        zoomOutFactor = 1 / zoomInFactor  # 缩小比例
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        print("mouseReleaseEvent from GraphicsView")
        # print(self.image_item.is_finish_cut, self.image_item.is_start_cut)
        if self.image_item.is_finish_cut:
            self.save_signal.emit(True)
        else:
            self.save_signal.emit(False)


class GraphicsPixmapItem(QGraphicsPixmapItem):
    save_signal = pyqtSignal(bool)

    def __init__(self, image):
        super().__init__()
        self.setPixmap(image)  # 设置图元内图像
        self.crop_box = CropBox()  # 自定义的裁剪框类
        self.is_start_cut = False  # 开始裁剪
        self.current_point = None
        self.start_point = None
        self.is_finish_cut = False

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        # self.setCursor(Qt.OpenHandCursor)
        print("mouseMoveEvent from GraphicsPixmapItem")
        self.current_point = event.pos()
        if not self.is_start_cut:
            self.moveBy(self.current_point.x() - self.start_point.x(),
                        self.current_point.y() - self.start_point.y())
            self.is_finish_cut = False
        self.update()

    # 鼠标按压事件
    def mousePressEvent(self, event):
        # self.setCursor(Qt.ClosedHandCursor)
        print("mousePressEvent from GraphicsPixmapItem")
        super(GraphicsPixmapItem, self).mousePressEvent(event)
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
    # self.setCursor(Qt.ArrowCursor)

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
