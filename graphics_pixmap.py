from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem


class GraphicsPixmapItem(QGraphicsPixmapItem):
    save_signal = pyqtSignal(bool)

    def __init__(self, image):
        super().__init__()
        self.setPixmap(image)  # 设置图元内图像
        self.setAcceptHoverEvents(True)  # 开启接受伪状态事件
        self.setFlag(QGraphicsItem.ItemIsSelectable)  # 设置允许选中
        self.current_point = None  # 鼠标当前坐标
        self.start_point = None  # 鼠标点击时的坐标

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        self.current_point = event.pos()
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
        self.setCursor(Qt.OpenHandCursor)
