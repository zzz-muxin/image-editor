from PyQt5.QtCore import Qt, QSizeF, QRectF, QPointF
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsItem


# 裁剪框类
class CropBox(QGraphicsItem):
    def __init__(self, pos, size, limit_rect, parent):
        try:
            super().__init__()
            self.setParentItem(parent)
            self.size = QSizeF(size)
            self.centerPen = QPen(Qt.gray, 2)
            self.centerBrush = QBrush(QColor(10, 10, 10, 100))
            self.cornerPen = QPen(Qt.black, 2)
            self.cornerSize = QSizeF(10, 10)  # 顶点尺寸
            self.cornerFix = None
            self.refreshCornerFix()
            self.cornerBrush = QBrush(Qt.white)

            self.dragFlag = None
            self.dragDiff = None
            self.minSize = QSizeF(30, 30)  # 裁剪框最小尺寸30 * 30
            self.limitRect = limit_rect  # 限制大小在pixmap_item中

            self.setPos(pos)
            self.setAcceptHoverEvents(True)  # 开启接受伪状态事件
        except Exception as e:
            print("Error:", e)

    # four corner rect in item
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

    # four corner point position in item
    def itemTopLeft(self):
        return QPointF(0, 0)

    def itemTopRight(self):
        return QPointF(self.size.width(), 0)

    def itemBottomLeft(self):
        return QPointF(0, self.size.height())

    def itemBottomRight(self):
        return QPointF(self.size.width(), self.size.height())

    # four corner point position in scene
    def parentTopLeft(self):
        # todo
        #print(self.mapToScene(self.itemTopLeft()).x(), (self.mapToScene(self.itemTopLeft()).y()))
        return self.mapToParent(self.itemTopLeft())

    def parentTopRight(self):
        return self.mapToParent(self.itemTopRight())

    def parentBottomLeft(self):
        return self.mapToParent(self.itemBottomLeft())

    def parentBottomRight(self):
        return self.mapToParent(self.itemBottomRight())

    #def parentItem(self):

    def refreshCornerFix(self):
        self.cornerFix = QPointF(self.cornerSize.width() / 2, self.cornerSize.height() / 2)

    # 可调整大小区域
    def boundingRect(self):
        try:
            return QRectF(-self.cornerFix, QSizeF(self.size) + self.cornerSize)
        except Exception as e:
            print("Error:", e)

    def paint(self, painter, option, widget=None):
        try:
            # draw center rect
            painter.setPen(self.centerPen)
            painter.setBrush(self.centerBrush)
            painter.drawRect(self.centerRect())

            # draw all four corner rect
            painter.setPen(self.cornerPen)
            painter.setBrush(self.cornerBrush)
            cornerXRadius = self.cornerFix.x()
            cornerYRadius = self.cornerFix.y()

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
                return
            if self.topRightCornerRect().contains(mousePressPos):
                self.dragFlag = "TOP_RIGHT"
                self.dragDiff = event.scenePos() - self.parentTopRight()
                return
            if self.bottomLeftCornerRect().contains(mousePressPos):
                self.dragFlag = "BOTTOM_LEFT"
                self.dragDiff = event.scenePos() - self.parentBottomLeft()
                return
            if self.bottomRightCornerRect().contains(mousePressPos):
                self.dragFlag = "BOTTOM_RIGHT"
                self.dragDiff = event.scenePos() - self.parentBottomRight()
                return
            if self.centerRect().contains(mousePressPos):
                self.dragFlag = "CENTER"
                self.dragDiff = event.scenePos() - self.parentTopLeft()
                return
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
            self.prepareGeometryChange()
            match self.dragFlag:
                case "TOP_LEFT":
                    parentTopLeft = mouseMovePos - self.dragDiff
                    parentBottomRight = self.parentBottomRight()

                    curTLX = parentTopLeft.x() if parentTopLeft.x() > xMinLimit else xMinLimit
                    curTLX = curTLX if parentBottomRight.x() - curTLX > minWidth else parentBottomRight.x() - minWidth

                    curTLY = parentTopLeft.y() if parentTopLeft.y() > yMinLimit else yMinLimit
                    curTLY = curTLY if parentBottomRight.y() - curTLY > minHeight else parentBottomRight.y() - minHeight

                    self.setPos(QPointF(curTLX, curTLY))
                    self.size = QSizeF(parentBottomRight.x() - curTLX, parentBottomRight.y() - curTLY)

                case "TOP_RIGHT":
                    parentTopRight = mouseMovePos - self.dragDiff
                    parentBottomLeft = self.parentBottomLeft()

                    curTRX = parentTopRight.x() if parentTopRight.x() < xMaxLimit else xMaxLimit
                    curTRX = curTRX if curTRX - parentBottomLeft.x() > minWidth else parentBottomLeft.x() + minWidth

                    curTRY = parentTopRight.y() if parentTopRight.y() > yMinLimit else yMinLimit
                    curTRY = curTRY if parentBottomLeft.y() - curTRY > minHeight else parentBottomLeft.y() - minHeight

                    self.setPos(QPointF(parentBottomLeft.x(), curTRY))
                    self.size = QSizeF(curTRX - parentBottomLeft.x(), parentBottomLeft.y() - curTRY)

                case "BOTTOM_LEFT":
                    parentBottomLeft = mouseMovePos - self.dragDiff
                    parentTopRight = self.parentTopRight()

                    curBLX = parentBottomLeft.x() if parentBottomLeft.x() > xMinLimit else xMinLimit
                    curBLX = curBLX if parentTopRight.x() - curBLX > minWidth else parentTopRight.x() - minWidth

                    curBLY = parentBottomLeft.y() if parentBottomLeft.y() < yMaxLimit else yMaxLimit
                    curBLY = curBLY if curBLY - parentTopRight.y() > minHeight else parentTopRight.y() + minHeight

                    self.setPos(QPointF(curBLX, parentTopRight.y()))
                    self.size = QSizeF(parentTopRight.x() - curBLX, curBLY - parentTopRight.y())

                case "BOTTOM_RIGHT":
                    parentBottomRight = mouseMovePos - self.dragDiff
                    parentTopLeft = self.parentTopLeft()

                    curBRX = parentBottomRight.x() if parentBottomRight.x() < xMaxLimit else xMaxLimit
                    curBRX = curBRX if curBRX - parentTopLeft.x() > minWidth else parentTopLeft.x() + minWidth

                    curBRY = parentBottomRight.y() if parentBottomRight.y() < yMaxLimit else yMaxLimit
                    curBRY = curBRY if curBRY - parentTopLeft.y() > minHeight else parentTopLeft.y() + minHeight

                    self.setPos(parentTopLeft)
                    self.size = QSizeF(curBRX - parentTopLeft.x(), curBRY - parentTopLeft.y())

                case "CENTER":
                    parentTopLeft = mouseMovePos - self.dragDiff

                    curTLX = parentTopLeft.x() if parentTopLeft.x() > xMinLimit else xMinLimit
                    curTLX = curTLX if curTLX + self.size.width() < xMaxLimit else xMaxLimit - self.size.width()
                    curTLY = parentTopLeft.y() if parentTopLeft.y() > yMinLimit else yMinLimit
                    curTLY = curTLY if curTLY + self.size.height() < yMaxLimit else yMaxLimit - self.size.height()

                    self.setPos(QPointF(curTLX, curTLY))
            self.update()
        except Exception as e:
            print("Error:", e)

    # 重写鼠标释放事件
    def mouseReleaseEvent(self, event):
        print("test")
        try:
            if event.button() == Qt.LeftButton:
                print("鼠标在SelectionBox里松开了！")
                self.dragFlag = None
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
    #         # 定义窗口的八个边界范围，用来调整窗口大小
    #         self._top_rect = None  # 顶部
    #         self._bottom_rect = None  # 底部
    #         self._left_rect = None  # 左侧
    #         self._right_rect = None  # 右侧
    #         self._left_top_rect = None  # 左上角
    #         self._right_top_rect = None  # 右上角
    #         self._left_bottom_rect = None  # 左下角
    #         self._right_bottom_rect = None  # 右下角
    #
    #         # 设置八个方向的鼠标拖拽放缩判断扳机默认值
    #         self._top_drag = False
    #         self._bottom_drag = False
    #         self._left_drag = False
    #         self._right_drag = False
    #         self._left_top_drag = False
    #         self._right_top_drag = False
    #         self._left_bottom_drag = False
    #         self._right_bottom_drag = False
    #         self._move_drag = False  # 鼠标拖拽移动扳机
    #         self.move_DragPosition = None  # 裁剪框拖拽坐标
    #
    #         self._padding = 8  # widget可拖拽调整大小区域宽度8px
    #     except Exception as e:
    #         print("Error:", e)
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
    # def resizeEvent(self, event):
    #     # 重新调整边界范围以备实现鼠标拖放缩放窗口大小，采用八个列表生成式生成八个坐标范围
    #     self._left_rect = [QPoint(x, y) for x in range(1, self._padding + 1)
    #                        for y in range(self._padding + 1, self.height() - self._padding)]
    #     self._right_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
    #                         for y in range(self._padding + 1, self.height() - self._padding)]
    #     self._top_rect = [QPoint(x, y) for x in range(self._padding + 1, self.width() - self._padding)
    #                       for y in range(1, self._padding + 1)]
    #     self._bottom_rect = [QPoint(x, y) for x in range(self._padding + 1, self.width() - self._padding)
    #                          for y in range(self.height() - self._padding, self.height() + 1)]
    #     self._right_bottom_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
    #                                for y in range(self.height() - self._padding, self.height() + 1)]
    #     self._left_bottom_rect = [QPoint(x, y) for x in range(1, self._padding + 1)
    #                               for y in range(self.height() - self._padding, self.height() + 1)]
    #     self._right_top_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
    #                             for y in range(1, self._padding + 1)]
    #     self._left_top_rect = [QPoint(x, y) for x in range(1, self._padding + 1)
    #                            for y in range(1, self._padding + 1)]
    #
    # # 重写鼠标点击事件
    # def mousePressEvent(self, event):
    #     # 鼠标左键按下
    #     if event.button() == Qt.LeftButton:
    #         self.left_button_clicked = True  # 开启鼠标左键点击标志
    #         if event.pos() in self._top_rect:
    #             # 鼠标左键点击上侧边界区域
    #             self._top_drag = True
    #             event.accept()
    #         elif event.pos() in self._bottom_rect:
    #             # 鼠标左键点击下侧边界区域
    #             self._bottom_drag = True
    #             event.accept()
    #         elif event.pos() in self._left_rect:
    #             # 鼠标左键点击左侧边界区域
    #             self._left_drag = True
    #             event.accept()
    #         elif event.pos() in self._right_rect:
    #             # 鼠标左键点击右侧边界区域
    #             self._right_drag = True
    #             event.accept()
    #         elif event.pos() in self._left_top_rect:
    #             # 鼠标左键点击左上角边界区域
    #             self._left_top_drag = True
    #             event.accept()
    #         elif event.pos() in self._right_bottom_rect:
    #             # 鼠标左键点击右下角边界区域
    #             self._right_bottom_drag = True
    #             event.accept()
    #         elif event.pos() in self._right_top_rect:
    #             # 鼠标左键点击右上角边界区域
    #             self._right_top_drag = True
    #             event.accept()
    #         elif event.pos() in self._left_bottom_rect:
    #             # 鼠标左键点击左下角边界区域
    #             self._left_bottom_drag = True
    #             event.accept()
    #         else:
    #             # 鼠标点击中间区域，进行移动
    #             self._move_drag = True  # 开启移动拖拽标志
    #             # 鼠标点击时的全局坐标 - 裁切框的左上角坐标 = 裁剪框的初始拖拽坐标
    #             self.move_DragPosition = event.globalPos() - self.pos()
    #             self.setCursor(Qt.ClosedHandCursor)
    #             event.accept()
    #
    # # 重写鼠标释放事件
    # def mouseReleaseEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         if self.cursor() == Qt.ClosedHandCursor:
    #             self.setCursor(Qt.OpenHandCursor)
    #         # 鼠标释放后各扳机复位
    #         self.left_button_clicked = False  # 关闭裁剪框被点击标志
    #
    #         self._top_drag = False
    #         self._bottom_drag = False
    #         self._left_drag = False
    #         self._right_drag = False
    #         self._left_top_drag = False
    #         self._right_top_drag = False
    #         self._left_bottom_drag = False
    #         self._right_bottom_drag = False
    #
    #         self._move_drag = False
    #     event.accept()
    #
    # # 重写鼠标移动事件
    # def mouseMoveEvent(self, event):
    #     point = event.pos()  # 获取鼠标相对于裁切框的坐标
    #     parent_point = self.mapToParent(point)  # 将鼠标事件的局部坐标映射到父级坐标系中的坐标
    #     # 鼠标没点击时，根据光标位置设置光标样式
    #     if not self.left_button_clicked:
    #         self._set_cursor(event.pos())
    #     # 调整窗口大小
    #     if Qt.LeftButton:
    #         if self._left_drag:
    #             # 左侧调整窗口宽度
    #             new_width = self.width() + (self.x() - event.globalPos().x())
    #             if new_width >= self.minimumWidth():
    #                 self.setGeometry(event.globalPos().x(), self.y(), new_width, self.height())
    #             event.accept()
    #         elif self._top_drag:
    #             # 顶部调整窗口高度
    #             new_height = self.height() + (self.y() - event.globalPos().y())
    #             if new_height >= self.minimumHeight():
    #                 self.setGeometry(self.x(), event.globalPos().y(), self.width(), new_height)
    #             event.accept()
    #         elif self._left_top_drag:
    #             # 左上角调整窗口大小
    #             new_width = self.width() + (self.x() - event.globalPos().x())
    #             new_height = self.height() + (self.y() - event.globalPos().y())
    #             if new_width >= self.minimumWidth() and new_height >= self.minimumHeight():
    #                 self.setGeometry(event.globalPos().x(), event.globalPos().y(), new_width, new_height)
    #             event.accept()
    #         elif self._right_top_drag:
    #             # 右上角调整窗口大小
    #             new_width = event.globalPos().x() - self.x()
    #             new_height = self.height() + (self.y() - event.globalPos().y())
    #             if new_width >= self.minimumWidth() and new_height >= self.minimumHeight():
    #                 self.setGeometry(self.x(), event.globalPos().y(), new_width, new_height)
    #             event.accept()
    #         elif self._left_bottom_drag:
    #             # 左下角调整窗口大小
    #             new_width = self.width() + (self.x() - event.globalPos().x())
    #             new_height = event.globalPos().y() - self.y()
    #             if new_width >= self.minimumWidth() and new_height >= self.minimumHeight():
    #                 self.setGeometry(event.globalPos().x(), self.y(), new_width, new_height)
    #             event.accept()
    #         # 仅对于右下的方向，可以用resize实现，更平滑
    #         elif self._right_drag:
    #             # 右侧调整窗口宽度
    #             self.resize(event.pos().x(), self.height())
    #             event.accept()
    #         elif self._bottom_drag:
    #             # 底部调整窗口高度
    #             self.resize(self.width(), event.pos().y())
    #             event.accept()
    #         elif self._right_bottom_drag:
    #             # 右下角同时调整高度和宽度
    #             self.resize(event.pos().x(), event.pos().y())
    #             event.accept()
    #         elif self._move_drag:
    #             # 拖动窗口
    #             self.move(event.globalPos() - self.move_DragPosition)
    #             event.accept()
    #
    # # 根据光标位置设置光标样式
    # def _set_cursor(self, point):
    #     if point in self._left_rect:
    #         # 左侧边界
    #         self.setCursor(Qt.SizeHorCursor)
    #     elif point in self._right_rect:
    #         # 右侧边界
    #         self.setCursor(Qt.SizeHorCursor)
    #     elif point in self._bottom_rect:
    #         # 底下边界
    #         self.setCursor(Qt.SizeVerCursor)
    #     elif point in self._top_rect:
    #         # 顶部边界
    #         self.setCursor(Qt.SizeVerCursor)
    #     elif point in self._left_top_rect:
    #         # 左上角边界
    #         self.setCursor(Qt.SizeFDiagCursor)
    #     elif point in self._left_bottom_rect:
    #         # 左下角边界
    #         self.setCursor(Qt.SizeBDiagCursor)
    #     elif point in self._right_top_rect:
    #         # 右上角边界
    #         self.setCursor(Qt.SizeBDiagCursor)
    #     elif point in self._right_bottom_rect:
    #         # 右下角边界
    #         self.setCursor(Qt.SizeFDiagCursor)
    #     else:
    #         self.setCursor(Qt.OpenHandCursor)
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


