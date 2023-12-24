import cv2
from PyQt5.QtGui import QPixmap, QColor, QFont
from PyQt5.QtCore import pyqtSignal, QPointF, QSizeF, Qt, QRectF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsTextItem, QWidget, \
    QTextEdit, QGraphicsProxyWidget, QGraphicsPixmapItem

from tools.image_format import ImageFormat


# 文本框类
class Text(QGraphicsTextItem):
    def __init__(self, parent: QGraphicsPixmapItem):
        super().__init__()
        self.parent = parent
        self.setParentItem(parent)  # 设置父QGraphicsPixmapItem
        self.setFlag(QGraphicsItem.ItemIsSelectable)  # 设置允许选中
        self.setFlag(QGraphicsTextItem.ItemIsFocusable)  # 允许获取焦点
        self.limitRect = QRectF(parent.pixmap().rect())  # 限制大小在父项pixmap中
        self.setPlainText("输入文字")  # 设置默认文本
        self.setDefaultTextColor(QColor(255, 255, 255))  # 设置默认字体颜色
        self.setFont(QFont("微软雅黑", 24))  # 设置默认字体

        self.setTextInteractionFlags(Qt.TextEditorInteraction)  # 启用文本编辑器交互
        self.setAcceptHoverEvents(True)  # 开启接受伪状态事件
        self.current_point = None  # 鼠标当前坐标
        self.start_point = None  # 鼠标点击时的坐标

        # 将文本初始位置设置在父项中心
        self._init_pos()

    def _init_pos(self):
        parent_center = self.limitRect.center()
        text_width = self.boundingRect().width()
        text_height = self.boundingRect().height()
        initial_x = parent_center.x() - text_width / 2
        initial_y = parent_center.y() - text_height / 2
        self.setPos(initial_x, initial_y)

    # 获取文本在父项的矩形
    def parent_rect(self):
        return self.mapRectToParent(self.boundingRect())

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        self.current_point = event.pos()
        # 计算移动后的位置
        new_x = self.pos().x() + (self.current_point.x() - self.start_point.x())
        new_y = self.pos().y() + (self.current_point.y() - self.start_point.y())
        # 获取父项的边界
        parent_rect = self.limitRect
        # 限制在父项的边界内
        new_x = max(parent_rect.left(), min(new_x, parent_rect.right() - self.boundingRect().width()))
        new_y = max(parent_rect.top(), min(new_y, parent_rect.bottom() - self.boundingRect().height()))
        # 移动文本框
        self.setPos(new_x, new_y)

    # 鼠标按压事件
    def mousePressEvent(self, event):
        super(QGraphicsTextItem, self).mousePressEvent(event)
        self.start_point = event.pos()

    # 鼠标释放事件
    # def mouseReleaseEvent(self, event):
    #     self.setCursor(Qt.OpenHandCursor)

    # 伪状态移动事件设置鼠标样式
    def hoverMoveEvent(self, event):
        self.setCursor(Qt.SizeAllCursor)
