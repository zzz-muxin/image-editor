from PyQt5.QtCore import Qt, QSizeF, QRectF, QPointF
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsItem


# 裁剪框类
class CropBox(QGraphicsItem):
    def __init__(self, size, limit_rect, parent):
        try:
            super().__init__()
            self.setParentItem(parent)  # 设置父QGraphicsPixmapItem
            self.size = QSizeF(size)  # 设置size为父Item中pixmap的大小
            self.minSize = QSizeF(50, 50)  # 裁剪框最小尺寸
            self.limitRect = limit_rect  # 限制大小在pixmap中
            self.PEN_RATIO = 1 / 100
            self.pen_size = int(max(self.size.width(), self.size.height()) * self.PEN_RATIO)
            print("pen size:", self.pen_size)

            self.centerPen = QPen(Qt.gray, self.pen_size)  # 中心矩形区域的笔
            self.cornerPen = QPen(Qt.black, self.pen_size)  # 四个顶点的笔
            self.cornerSize = QSizeF(self.pen_size * 5, self.pen_size * 5)  # 顶点尺寸
            self.cornerFix = None
            self.refreshCornerFix()
            self.cornerBrush = QBrush(Qt.white)

            self.dragFlag = None  # 拖拽的方向标志
            self.dragDiff = None  # 拖拽的坐标

            #self.setPos(self.mapToParent(self.itemTopRight()))
            #print(self.pos.x(), self.pos.y())
            self.setAcceptHoverEvents(True)  # 开启接受伪状态事件
        except Exception as e:
            print("Error:", e)

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

    def refreshCornerFix(self):
        self.cornerFix = QPointF(self.cornerSize.width() / 2, self.cornerSize.height() / 2)

    # 可调整大小区域圆点
    def boundingRect(self):
        try:
            return QRectF(-self.cornerFix, QSizeF(self.size) + self.cornerSize)
        except Exception as e:
            print("Error:", e)

    # 绘制裁剪框
    def paint(self, painter, option, widget=None):
        try:
            # 绘制中心的矩形
            painter.setPen(self.centerPen)
            painter.setBrush(QBrush(QColor(10, 10, 10, 100)))
            painter.drawRect(self.centerRect())

            # 绘制裁剪框内部虚线
            pen = QPen(QColor(255, 255, 255), self.pen_size, Qt.DashLine)  # 白色，笔宽1，虚线
            painter.setPen(pen)
            # 绘制2条垂直虚线
            for i in range(1, 3):
                width = self.getWidth() // 3
                height = self.getHeight()
                painter.drawLine(int(i * width), 0, int(i * width), int(height))
            # 绘制2条水平虚线
            for i in range(1, 3):
                width = self.getWidth()
                height = self.getHeight() // 3
                painter.drawLine(0, int(i * height), int(width), int(i * height))

            # 绘制四个顶点
            painter.setPen(self.cornerPen)
            painter.setBrush(self.cornerBrush)
            cornerXRadius = self.cornerFix.x()
            cornerYRadius = self.cornerFix.y()

            # 使用圆角矩形绘制
            painter.drawRoundedRect(self.topLeftCornerRect(), cornerXRadius, cornerYRadius)  # top left
            painter.drawRoundedRect(self.topRightCornerRect(), cornerXRadius, cornerYRadius)  # top right
            painter.drawRoundedRect(self.bottomLeftCornerRect(), cornerXRadius, cornerYRadius)  # bottom left
            painter.drawRoundedRect(self.bottomRightCornerRect(), cornerXRadius, cornerYRadius)  # bottom right
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
        try:
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
            #event.accept()
        except Exception as e:
            print("Error:", e)

    # 重写鼠标移动事件
    def mouseMoveEvent(self, event):
        try:
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
            event.accept()
        except Exception as e:
            print("Error:", e)

    # 重写鼠标释放事件
    def mouseReleaseEvent(self, event):
        print("test")
        try:
            if event.button() == Qt.LeftButton:
                print("鼠标在SelectionBox里松开了！")
                self.dragFlag = None
                event.accept()
        except Exception as e:
            print("Error:", e)

    def setState(self, pos, size):
        try:
            self.setPos(QPointF(pos))
            self.size = QSizeF(size)
        except Exception as e:
            print("Error:", e)

    def setSize(self, size):
        self.size = QSizeF(size)

    def setLimit(self, limit: QRectF):
        self.limitRect = limit

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


            # def __init__(self, pixmap, parent=None):
    #     try:
    #         super().__init__(parent)
    #         # self.min_width = 80  # 最小宽度
    #         # self.min_height = 80  # 最小高度
    #         self.left_button_clicked = False  # 裁剪框被鼠标左键点击标志
    #         # self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)  # 透明背景
    #         #self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏系统边框
    #         #self.setMouseTracking(True)  # 开启鼠标追踪
    #         self.pixmap = pixmap
    #         self.draw_border()
    #         #self.setParentItem(parent)
    #

    #
    # # 绘制事件
    # # def paintEvent(self, event):
    # #     try:
    # #         print("CropBox paint!")
    # #         painter = QPainter(self)
    # #         self.draw_internal_lines(painter)  # 绘制裁剪框内部虚线
    # #         self.draw_border(painter)  # 绘制裁剪框边框实线
    # #         # self.draw_border_points(painter)  # 绘制边框上八个方向的顶点
    # #         # self.draw_size_text(painter)  # 绘制当前裁剪框像素大小文本
    # #     except Exception as e:
    # #         print("Error:paintEvent", e)
    #
    #
    #

    # # 绘制裁剪框边框实线
    # def draw_border(self):
    #     try:
    #         print("draw_border")
    #         # painter = QPainter(self)
    #         rect = QRectF(self.pixmap.rect())
    #         pen = QPen(QColor(3, 125, 203), 5)  # 笔线宽5个像素
    #         # painter.setPen(pen)
    #         # painter.drawRect(rect)
    #         self.path = QPainterPath()
    #         self.path.addRect(rect)
    #         self.setPath(self.path)
    #     except Exception as e:
    #         print("Error: draw_border", e)
    #
    # # 绘制边框上八个方向的顶点
    # def draw_border_points(self, painter):
    #     pen = QPen(QColor(3, 125, 203), 5)  # 笔线宽5个像素
    #     painter.setPen(pen)
    #     painter.drawPoint(2, 2)  # 左上角
    #     painter.drawPoint(self.width() // 2, 2)  # 顶部
    #     painter.drawPoint(self.width() - 2, 2)  # 右上角
    #     painter.drawPoint(2, self.height() // 2)  # 左侧
    #     painter.drawPoint(2, self.height() - 2)  # 左下角
    #     painter.drawPoint(self.width() - 2, self.height() // 2)  # 右侧
    #     painter.drawPoint(self.width() - 2, self.height() - 2)  # 右下角
    #     painter.drawPoint(self.width() // 2, self.height() - 2)  # 底部
    #
    # # 绘制裁剪框内部虚线
    # def draw_internal_lines(self, painter):
    #     crop_box_path = QPainterPath()  # 绘图区域
    #     crop_box_path.addRect(2, 2, self.width() - 4, self.height() - 4)  # 添加矩形区域
    #     painter.setClipPath(crop_box_path)  # 设置被限制的绘画区域为crop_box_path
    #     painter.setClipping(True)  # 启用剪切限制
    #     # 绘画内部虚线线条
    #     pen = QPen(QColor(230, 230, 230), 1, Qt.DashLine)  # 笔线宽1，为虚线
    #     painter.setPen(pen)
    #     # 绘制2条垂直虚线
    #     for i in range(1, 3):
    #         width = self.width() // 3
    #         painter.drawLine(i * width, 2, i * width, self.height() - 2)
    #     # 绘制2条水平虚线
    #     for i in range(1, 3):
    #         height = self.height() // 3
    #         painter.drawLine(2, i * height, self.width() - 2, i * height)
    #     # 绘画完，取消被限制的区域
    #     painter.setClipping(False)
    #
    # # 绘制当前裁剪框像素大小文本
    # def draw_size_text(self, painter):
    #     # 通过在裁剪框底部开辟一块矩形区来实现
    #     pen = QPen(QColor(255, 0, 0))  # 红笔
    #     painter.setPen(pen)
    #     size_text = f"({self.width()}, {self.height()})"  # 使用f-string格式化字符串
    #     top_left = QPointF(self.width() - self.min_width, self.height() - 20)  # 文本绘制区域的左上角坐标
    #     size = QSizeF(self.min_width, 20)
    #     rect = QRectF(top_left, size)
    #     option = QTextOption()  # 文本垂直方向居中对齐，水平方向右对齐
    #     painter.drawText(rect, size_text, option)


