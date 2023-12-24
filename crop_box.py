from PyQt5.QtCore import Qt, QSizeF, QRectF, QPointF
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem


# 裁剪框类
class CropBox(QGraphicsItem):
    def __init__(self, parent: QGraphicsPixmapItem):
        super().__init__()
        self.parent = parent
        self.setParentItem(parent)  # 设置父QGraphicsPixmapItem
        self.size = QSizeF(parent.pixmap().size())  # 设置size为父Item中pixmap的大小
        self.minSize = QSizeF(1, 1)  # 裁剪框最小尺寸
        self.limitRect = QRectF(parent.pixmap().rect())  # 限制大小在pixmap中
        self.PEN_RATIO = 1 / 100  # 设置裁剪框笔的大小为图片大小的1/100
        self.pen_size = self.update_pen_size()
        print("pen size:", self.pen_size)

        self.centerPen = QPen(Qt.gray, self.pen_size)  # 中心矩形区域的笔
        self.cornerPen = QPen(Qt.black, self.pen_size)  # 四个顶点的笔
        self.cornerSize = QSizeF(self.pen_size * 5, self.pen_size * 5)  # 顶点尺寸
        self.cornerFix = None
        self.refreshCornerFix()
        self.cornerBrush = QBrush(Qt.white)

        self.dragFlag = None  # 拖拽的方向标志
        self.dragDiff = None  # 拖拽的坐标

        self.setAcceptHoverEvents(True)  # 开启接受伪状态事件

    # 更新笔的大小
    def update_pen_size(self):
        pen_size = max(self.size.width(), self.size.height()) * self.PEN_RATIO
        if pen_size > 0:
            return pen_size
        else:
            return 1

    # 四个corner的rect
    def centerRect(self):
        return QRectF(self.itemTopLeft(), QSizeF(self.size))

    def topLeftCornerRect(self):
        return QRectF(self.itemTopLeft() - self.cornerFix, self.cornerSize)

    def topRightCornerRect(self):
        return QRectF(self.itemTopRight() - self.cornerFix, self.cornerSize)

    def bottomLeftCornerRect(self):
        return QRectF(self.itemBottomLeft() - self.cornerFix, self.cornerSize)

    def bottomRightCornerRect(self):
        return QRectF(self.itemBottomRight() - self.cornerFix, self.cornerSize)

    # 矩形的四个顶点坐标
    def itemTopLeft(self):
        return QPointF(0, 0)

    def itemTopRight(self):
        return QPointF(self.size.width(), 0)

    def itemBottomLeft(self):
        return QPointF(0, self.size.height())

    def itemBottomRight(self):
        return QPointF(self.size.width(), self.size.height())

    # 四个顶点的坐标映射到父坐标系中
    def parentTopLeft(self):
        return self.mapToParent(self.itemTopLeft())

    def parentTopRight(self):
        return self.mapToParent(self.itemTopRight())

    def parentBottomLeft(self):
        return self.mapToParent(self.itemBottomLeft())

    def parentBottomRight(self):
        return self.mapToParent(self.itemBottomRight())

    # 获取裁剪区域在parentItem中的矩形
    def parentRect(self):
        return self.mapRectToParent(self.centerRect())

    # 获取裁剪框左上角点在场景中的位置
    def getSceneTopLeft(self):
        return self.mapToScene(self.itemTopLeft())

    # 圆形顶点大小
    def refreshCornerFix(self):
        self.cornerFix = QPointF(self.cornerSize.width() / 2, self.cornerSize.height() / 2)

    # 边界区域
    def boundingRect(self):
        return QRectF(-self.cornerFix, QSizeF(self.size) + self.cornerSize)

    # 绘制
    def paint(self, painter, option, widget=None):
        try:
            # 绘制中心的矩形
            painter.setPen(self.centerPen)
            painter.drawRect(self.centerRect())

            # 绘制裁剪框内部虚线
            pen = QPen(QColor(255, 255, 255, 150), self.pen_size, Qt.DashLine)  # 白色，笔宽，虚线
            painter.setPen(pen)
            # 绘制2条垂直虚线
            for i in range(1, 3):
                width = self.getWidth() / 3
                height = self.getHeight()
                painter.drawLine(int(i * width), 0, int(i * width), int(height))
            # 绘制2条水平虚线
            for i in range(1, 3):
                width = self.getWidth()
                height = self.getHeight() / 3
                painter.drawLine(0, int(i * height), int(width), int(i * height))

            # 绘制四个顶点
            painter.setPen(self.cornerPen)
            painter.setBrush(self.cornerBrush)
            cornerXRadius = self.cornerFix.x()
            cornerYRadius = self.cornerFix.y()
            # 使用圆角矩形绘制圆点
            painter.drawRoundedRect(self.topLeftCornerRect(), cornerXRadius, cornerYRadius)  # top left
            painter.drawRoundedRect(self.topRightCornerRect(), cornerXRadius, cornerYRadius)  # top right
            painter.drawRoundedRect(self.bottomLeftCornerRect(), cornerXRadius, cornerYRadius)  # bottom left
            painter.drawRoundedRect(self.bottomRightCornerRect(), cornerXRadius, cornerYRadius)  # bottom right

            # 绘制阴影遮罩
            # painter.setPen(Qt.NoPen)
            # painter.setBrush(QColor(0, 0, 0, 155))
            # todo
        except Exception as e:
            print("Error:", e)

    # 伪状态移动事件设置鼠标样式
    def hoverMoveEvent(self, event):
        try:
            if self.topLeftCornerRect().contains(event.pos()) or self.bottomRightCornerRect().contains(event.pos()):
                self.setCursor(Qt.SizeFDiagCursor)
                return
            if self.topRightCornerRect().contains(event.pos()) or self.bottomLeftCornerRect().contains(event.pos()):
                self.setCursor(Qt.SizeBDiagCursor)
                return
            if self.centerRect().contains(event.pos()):
                self.setCursor(Qt.SizeAllCursor)
                return
            self.setCursor(Qt.ArrowCursor)
        except Exception as e:
            print("Error:", e)

    # 重写鼠标点击事件
    def mousePressEvent(self, event):
        mousePressPos = event.pos()
        if self.topLeftCornerRect().contains(mousePressPos):
            self.dragFlag = "TOP_LEFT"
            self.dragDiff = event.scenePos() - self.parentTopLeft()
        elif self.topRightCornerRect().contains(mousePressPos):
            self.dragFlag = "TOP_RIGHT"
            self.dragDiff = event.scenePos() - self.parentTopRight()
        elif self.bottomLeftCornerRect().contains(mousePressPos):
            self.dragFlag = "BOTTOM_LEFT"
            self.dragDiff = event.scenePos() - self.parentBottomLeft()
        elif self.bottomRightCornerRect().contains(mousePressPos):
            self.dragFlag = "BOTTOM_RIGHT"
            self.dragDiff = event.scenePos() - self.parentBottomRight()
        elif self.centerRect().contains(mousePressPos):
            self.dragFlag = "CENTER"
            self.dragDiff = event.scenePos() - self.parentTopLeft()
        event.accept()

    # 重写鼠标移动事件
    def mouseMoveEvent(self, event):
        mouseMovePos = event.scenePos()
        xMinLimit = self.limitRect.x()
        xMaxLimit = xMinLimit + self.limitRect.width()
        yMinLimit = self.limitRect.y()
        yMaxLimit = yMinLimit + self.limitRect.height()
        minWidth = self.minSize.width()
        minHeight = self.minSize.height()
        self.prepareGeometryChange()  # 预备重新绘制裁剪框
        match self.dragFlag:
            case "TOP_LEFT":
                # 左上角拖拽
                parentTopLeft = mouseMovePos - self.dragDiff
                parentBottomRight = self.parentBottomRight()

                curTLX = parentTopLeft.x() if parentTopLeft.x() > xMinLimit else xMinLimit
                curTLX = curTLX if parentBottomRight.x() - curTLX > minWidth else parentBottomRight.x() - minWidth

                curTLY = parentTopLeft.y() if parentTopLeft.y() > yMinLimit else yMinLimit
                curTLY = curTLY if parentBottomRight.y() - curTLY > minHeight else parentBottomRight.y() - minHeight

                self.setPos(QPointF(curTLX, curTLY))
                self.size = QSizeF(parentBottomRight.x() - curTLX, parentBottomRight.y() - curTLY)

            case "TOP_RIGHT":
                # 右上角拖拽
                parentTopRight = mouseMovePos - self.dragDiff
                parentBottomLeft = self.parentBottomLeft()

                curTRX = parentTopRight.x() if parentTopRight.x() < xMaxLimit else xMaxLimit
                curTRX = curTRX if curTRX - parentBottomLeft.x() > minWidth else parentBottomLeft.x() + minWidth

                curTRY = parentTopRight.y() if parentTopRight.y() > yMinLimit else yMinLimit
                curTRY = curTRY if parentBottomLeft.y() - curTRY > minHeight else parentBottomLeft.y() - minHeight

                self.setPos(QPointF(parentBottomLeft.x(), curTRY))
                self.size = QSizeF(curTRX - parentBottomLeft.x(), parentBottomLeft.y() - curTRY)

            case "BOTTOM_LEFT":
                # 左下角拖拽
                parentBottomLeft = mouseMovePos - self.dragDiff
                parentTopRight = self.parentTopRight()

                curBLX = parentBottomLeft.x() if parentBottomLeft.x() > xMinLimit else xMinLimit
                curBLX = curBLX if parentTopRight.x() - curBLX > minWidth else parentTopRight.x() - minWidth

                curBLY = parentBottomLeft.y() if parentBottomLeft.y() < yMaxLimit else yMaxLimit
                curBLY = curBLY if curBLY - parentTopRight.y() > minHeight else parentTopRight.y() + minHeight

                self.setPos(QPointF(curBLX, parentTopRight.y()))
                self.size = QSizeF(parentTopRight.x() - curBLX, curBLY - parentTopRight.y())

            case "BOTTOM_RIGHT":
                # 右下角拖拽
                parentBottomRight = mouseMovePos - self.dragDiff
                parentTopLeft = self.parentTopLeft()

                curBRX = parentBottomRight.x() if parentBottomRight.x() < xMaxLimit else xMaxLimit
                curBRX = curBRX if curBRX - parentTopLeft.x() > minWidth else parentTopLeft.x() + minWidth

                curBRY = parentBottomRight.y() if parentBottomRight.y() < yMaxLimit else yMaxLimit
                curBRY = curBRY if curBRY - parentTopLeft.y() > minHeight else parentTopLeft.y() + minHeight

                self.setPos(parentTopLeft)
                self.size = QSizeF(curBRX - parentTopLeft.x(), curBRY - parentTopLeft.y())

            case "CENTER":
                # 中心区域进行移动
                parentTopLeft = mouseMovePos - self.dragDiff

                curTLX = parentTopLeft.x() if parentTopLeft.x() > xMinLimit else xMinLimit
                curTLX = curTLX if curTLX + self.size.width() < xMaxLimit else xMaxLimit - self.size.width()
                curTLY = parentTopLeft.y() if parentTopLeft.y() > yMinLimit else yMinLimit
                curTLY = curTLY if curTLY + self.size.height() < yMaxLimit else yMaxLimit - self.size.height()

                self.setPos(QPointF(curTLX, curTLY))
        self.update()  # 更新绘制
        self.updateState()
        event.accept()

    # 重写鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.dragFlag = None
        event.accept()

    def setState(self, pos, size):
        try:
            self.setPos(QPointF(pos))
            self.size = QSizeF(size)
        except Exception as e:
            print("Error:", e)

    # 更新裁剪框状态
    def updateState(self):
        self.prepareGeometryChange()
        self.pen_size = self.update_pen_size()
        self.centerPen = QPen(Qt.gray, self.pen_size)  # 中心矩形区域的笔
        self.cornerPen = QPen(Qt.black, self.pen_size)  # 四个顶点的笔
        self.cornerSize = QSizeF(self.pen_size * 5, self.pen_size * 5)  # 顶点尺寸
        self.refreshCornerFix()
        self.limitRect = QRectF(self.parent.pixmap().rect())
        self.update()

    # 更新裁剪框大小和位置
    def update_pos(self):
        self.setPos(0, 0)
        self.size = QSizeF(self.parent.pixmap().size())  # 设置size为父Item中pixmap的大小
        self.updateState()

    def setSize(self, size):
        self.size = QSizeF(size)

    def setLimit(self, limit_rect: QRectF):
        self.limitRect = limit_rect

    def getState(self):
        return self.pos(), self.size

    def getPos(self):
        return self.pos()

    def getX(self):
        return self.pos().x()

    def getY(self):
        return self.pos().y()

    def getWidth(self):
        return self.size.width()

    def getHeight(self):
        return self.size.height()

