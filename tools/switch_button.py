from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QRect, QRectF, QThread
from PyQt5.QtGui import QColor, QMouseEvent, QPaintEvent, QPainter, QPainterPath, QPen, QFont
from PyQt5.QtWidgets import QWidget


# 开关按钮
class SwitchButton(QWidget):
    clickedOn = pyqtSignal()
    clickedOff = pyqtSignal()

    def __init__(self, parent=None):
        super(SwitchButton, self).__init__(parent)
        super(SwitchButton, self).setFixedWidth(50)
        super(SwitchButton, self).setFixedHeight(24)
        self.step = self.width() / 100  # 每次移动的步长为宽度的50分之一

        # 色彩设置（缺省）
        self.backgroundColorOff = QColor(135, 135, 135)
        self.backgroundColorOn = QColor(0, 200, 0)

        # 滑块颜色（缺省）
        self.sliderColorOff = QColor(255, 255, 255)
        self.sliderColorOn = QColor(255, 255, 255)

        # 文本颜色（缺省）
        self.textColorOff = QColor(0, 0, 0)
        self.textColorOn = QColor(0, 0, 0)

        # 初始化文本（缺省）
        self.textOn = ""
        self.textOff = ""
        self.setFont(QFont("Microsoft Yahei", 9))

        # 当前状态
        self.state = False

        # 内部⚪的大小（缺省）
        self.space = 3
        self.rectRadius = 4

        # 运动坐标初始化
        self.startX = 0
        self.endX = 0

        # 时钟初始化
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self._updateValue)  # 计时结束调用operate()方法

    def setGeometry(self, *args, **kwargs):
        super(SwitchButton, self).setGeometry(*args, **kwargs)
        # 每次移动的步长为宽度的50分之一
        self.step = self.width() / 100
        font = QFont()
        font.setPixelSize(int(0.3 * self.width()))
        font.setFamily("黑体")
        self.setFont(font)

    def mousePressEvent(self, event):  # 鼠标时间
        self.state = not self.state

        # 状态切换改变后自动计算终点坐标
        if self.state:
            # 发射信号
            self.clickedOn.emit()
            self.endX = self.width() - self.height()
        else:
            # 发射信号
            self.clickedOff.emit()
            self.endX = 0
        self.timer.start(5)

    def paintEvent(self, event: QPaintEvent):  # 绘制事件
        # 绘制实例化
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        painter.begin(self)

        # 绘制背景
        self._drawBackground(event, painter)

        # 绘制滑块
        self._drawSlider(event, painter)

        # 绘制文字
        self._drawText(event, painter)

        # 绘制结束
        painter.end()

    # 设置关闭状态下背景颜色
    def setBackgroundColorOff(self, color: QColor):
        self.backgroundColorOff = color

    # 设置开启状态下背景颜色
    def setBackgroundColorOn(self, color: QColor):
        self.backgroundColorOn = color

    # 设置关闭状态下滑块颜色
    def setSliderColorOff(self, color: QColor):
        self.sliderColorOff = color

    # 设置开启状态下滑块颜色
    def setSliderColorOn(self, color: QColor):
        self.sliderColorOn = color

    # 设置开启状态下文本颜色
    def setTextColorOn(self, color: QColor):
        self.textColorOn = color

    # 设置关闭状态下文本颜色
    def setTextColorOff(self, color: QColor):
        self.textColorOff = color

    # 设置开启状态下文本
    def setTextOn(self, text: str):
        self.textOn = text

    # 设置关闭状态下文本
    def setTextOff(self, text: str):
        self.textOff = text

    # 强制开启，使用信号触发
    def setOn(self) -> bool:
        if not self.state:
            self.mousePressEvent()
        return self.state

    # 强制关闭，使用信号触发
    def setOff(self) -> bool:
        if self.state:
            self.mousePressEvent()
        return self.state

    # 设置滑动速度
    def setSpeed(self, speed: int):
        self.step = self.width() / speed

    # 设置滑快边距，改变滑块大小
    def setMargin(self, margin: int):
        self.space = margin

    # 获取当前开关状态
    def getState(self) -> bool:
        return self.state

    def _drawBackground(self, event, painter):
        painter.save()
        painter.setPen(Qt.NoPen)

        if self.state and self.startX == self.endX:  # 打开时
            painter.setBrush(self.backgroundColorOn)
        else:  # 关闭时
            painter.setBrush(self.backgroundColorOff)

        # 矩形区域位置及长宽，位置不用管
        rect = QRect(0, 0, self.width(), self.height())
        # ⚪的半径为高度的一半
        radius = rect.height() // 2
        # ⚪的宽度为高度
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())
        painter.drawPath(path)
        painter.restore()

    def _drawSlider(self, event, painter):
        painter.save()
        pen = QPen(self.sliderColorOn, -1)
        painter.setPen(pen)
        if self.state:
            # 填充颜色
            painter.setBrush(self.sliderColorOn)
        else:
            # 填充颜色
            painter.setBrush(self.sliderColorOff)

        rect = QRect(0, 0, self.width(), self.height())

        # 滑块距离背景的间隙
        sliderWidth = rect.height() - self.space * 2

        # 滑块的位置，及滑块的形状
        sliderRect = QRect(int(self.startX + self.space), int(self.space), int(sliderWidth), int(sliderWidth))

        # 绘制椭圆
        painter.drawEllipse(sliderRect)

        # 恢复
        painter.restore()

    def _drawText(self, event, painter):
        painter.save()

        if self.state and self.startX == self.endX:
            painter.setPen(self.textColorOn)
            painter.drawText(0, 0, int(self.width() / 2 + self.space * 2), int(self.height()), Qt.AlignCenter,
                             self.textOn)
        else:
            if self.startX == 0:
                painter.setPen(self.textColorOff)
                painter.drawText(int(self.width() / 2), 0, int(self.width() / 2 - self.space), int(self.height()),
                                 Qt.AlignCenter,
                                 self.textOff)

        painter.restore()

    def _updateValue(self):  # 运动坐标更新
        if self.state:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        self.update()
