from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QEnterEvent
from PyQt5.QtWidgets import QMainWindow, QGraphicsPixmapItem

from adjust_area import AdjustArea
from function_stack import FunctionStack
from graphics_view import GraphicsView
from mainwindow import Ui_MainWindow
from upload_image import UploadImageWidget


class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # 设置ui

        # 定义窗口的八个边界范围，用来调整窗口大小
        self._top_rect = None  # 顶部
        self._bottom_rect = None  # 底部
        self._left_rect = None  # 左侧
        self._right_rect = None  # 右侧
        self._left_top_rect = None  # 左上角
        self._right_top_rect = None  # 右上角
        self._left_bottom_rect = None  # 左下角
        self._right_bottom_rect = None  # 右下角

        # 设置八个方向的鼠标拖拽跟踪判断扳机默认值
        self._top_drag = False
        self._bottom_drag = False
        self._left_drag = False
        self._right_drag = False
        self._left_top_drag = False
        self._right_top_drag = False
        self._left_bottom_drag = False
        self._right_bottom_drag = False

        self.move_DragPosition = None  # 鼠标拖拽坐标
        self._move_drag = False  # 鼠标拖拽窗口移动扳机
        self.left_button_clicked = False  # 鼠标左键点击标志

        self._padding = 8  # 主窗口可拖拽调整大小区域宽度8px

        # 设置各组件开启鼠标跟踪
        self.setMouseTracking(True)
        self.frame.setMouseTracking(True)
        self.frame_menu.setMouseTracking(True)
        self.frame_function.setMouseTracking(True)
        self.widget_view.setMouseTracking(True)
        self.main_stacked_widget.setMouseTracking(True)
        # 初始化事件过滤器
        self.frame.installEventFilter(self)
        self.frame_menu.installEventFilter(self)
        self.frame_function.installEventFilter(self)
        self.widget_view.installEventFilter(self)
        self.main_stacked_widget.installEventFilter(self)
        print("main window size:", self.width(), self.height())

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)  # 透明背景
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏系统边框
        self.effect_shadow_style(self.frame_menu)  # 设置菜单栏阴影
        self.effect_shadow_style(self.frame_function)  # 设置功能栏阴影
        self.pushButton_close.clicked.connect(self.close)  # 关闭按钮
        self.pushButton_max_and_reduction.clicked.connect(self.toggle_maximize)  # 最大化（还原）按钮
        self.pushButton_min.clicked.connect(self.showMinimized)  # 最小化按钮

        self.graphicsView = None  # 初始化图像显示视图
        self._init_all_widget()  # 初始化所有组件的事件

    # 初始化所有组件的事件
    def _init_all_widget(self):
        self.function_stack = FunctionStack()
        self.adjust_area = AdjustArea()
        self.pushButton_crop.clicked.connect(self._init_button_crop)
        self.pushButton_rotate.clicked.connect(self._init_button_rotate)
        self.pushButton_adjust.clicked.connect(self._init_button_adjust)

        uploader = UploadImageWidget()
        self.horizontalLayout_upload.addWidget(uploader)  # 添加自定义的上传图片UploadImageWidget类
        uploader.image_exist.connect(self.show_image)  # 连接到图片显示方法

        # 一个垂直布局套一个水平布局
        self.horizontalLayout_adjust_view = QtWidgets.QHBoxLayout()
        self.horizontalLayout_adjust_view.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_adjust_view.setObjectName("horizontalLayout_adjust_view")
        self.verticalLayout_image_view = QtWidgets.QVBoxLayout()
        self.verticalLayout_image_view.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_image_view.setObjectName("verticalLayout_image_view")
        self.verticalLayout_image_view.addLayout(self.horizontalLayout_adjust_view)
        self.verticalLayout_image_view.setStretch(0, 1)
        self.verticalLayout_image_view.addWidget(self.function_stack)
        self.function_stack.hide()

    # 图片显示方法
    def show_image(self, pixmap):
        self.graphicsView = GraphicsView(pixmap, self)  # 查看图片的GraphicsView
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭垂直滑动条
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭水平滑动条
        self.page_image_view.setLayout(self.verticalLayout_image_view)  # 设置垂直布局
        self.horizontalLayout_adjust_view.addWidget(self.graphicsView)  # 添加graphicsView到布局
        self.horizontalLayout_adjust_view.setStretch(0, 2)

        self.graphicsView.scale_signal.connect(self.show_label_scale)  # 连接到图片缩放比例显示方法

        self.main_stacked_widget.setCurrentIndex(1)  # 跳转到图片视图界面

    # 图片缩放比例显示方法
    def show_label_scale(self, scale):
        show_scale = int(scale * 100)  # 转为int
        self.label_scale.setText(f"{show_scale: .0f}%")  # 用f-string格式化输出

    def _init_button_adjust(self):
        # 检查graphicsView视图内是否存在图片
        if self.graphicsView is not None:
            for item in self.graphicsView.items():
                if isinstance(item, QGraphicsPixmapItem):
                    # 存在图片才显示adjust_area
                    self.main_stacked_widget.setCurrentIndex(1)
                    self.horizontalLayout_adjust_view.addWidget(self.adjust_area)
                    self.horizontalLayout_adjust_view.setStretch(1, 1)
                    self.adjust_area.show()
                    self.function_stack.hide()

    def _init_button_rotate(self):
        # 检查graphicsView视图内是否存在图元
        if self.graphicsView is not None:
            for item in self.graphicsView.items():
                if isinstance(item, QGraphicsPixmapItem):
                    self.main_stacked_widget.setCurrentIndex(1)
                    self.function_stack.basic_function_stack.setCurrentIndex(1)
                    self.adjust_area.hide()
                    self.function_stack.show()

    def _init_button_crop(self):
        # 检查graphicsView视图内是否存在图片
        if self.graphicsView is not None:
            for item in self.graphicsView.items():
                if isinstance(item, QGraphicsPixmapItem):
                    self.main_stacked_widget.setCurrentIndex(1)
                    self.function_stack.basic_function_stack.setCurrentIndex(0)
                    if self.graphicsView.pixmap_item.is_start_cut:
                        self.graphicsView.pixmap_item.is_start_cut = False
                        self.graphicsView.pixmap_item.setCursor(Qt.ArrowCursor)  # 箭头光标
                    else:
                        self.graphicsView.pixmap_item.is_start_cut = True
                        self.graphicsView.pixmap_item.setCursor(Qt.CrossCursor)  # 十字光标
                    self.adjust_area.hide()
                    self.function_stack.show()

    # 事件过滤器
    def eventFilter(self, obj, event):
        # 用于鼠标进入其他控件后还原为标准箭头光标样式
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super(AppWindow, self).eventFilter(obj, event)

    # 计算窗口边界
    def resizeEvent(self, event):
        # 重新调整边界范围以备实现鼠标拖放缩放窗口大小，采用八个列表生成式生成八个坐标范围
        self._left_rect = [QPoint(x, y) for x in range(1, self._padding + 1)
                           for y in range(self._padding + 1, self.height() - self._padding)]
        self._right_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                            for y in range(self._padding + 1, self.height() - self._padding)]
        self._top_rect = [QPoint(x, y) for x in range(self._padding + 1, self.width() - self._padding)
                          for y in range(1, self._padding + 1)]
        self._bottom_rect = [QPoint(x, y) for x in range(self._padding + 1, self.width() - self._padding)
                             for y in range(self.height() - self._padding, self.height() + 1)]
        self._right_bottom_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                                   for y in range(self.height() - self._padding, self.height() + 1)]
        self._left_bottom_rect = [QPoint(x, y) for x in range(1, self._padding + 1)
                                  for y in range(self.height() - self._padding, self.height() + 1)]
        self._right_top_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                                for y in range(1, self._padding + 1)]
        self._left_top_rect = [QPoint(x, y) for x in range(1, self._padding + 1)
                               for y in range(1, self._padding + 1)]

    # 阴影样式
    def effect_shadow_style(self, widget):
        effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(0, 0)  # 偏移
        effect_shadow.setBlurRadius(30)  # 阴影半径
        effect_shadow.setColor(QColor(0, 0, 0))  # 阴影颜色
        widget.setGraphicsEffect(effect_shadow)

    # 最大化（还原）按钮实现
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.pushButton_max_and_reduction.setMinimumSize(48, 44)
            self.pushButton_max_and_reduction.setToolTip("最大化")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/images/icon/maximize_expand_icon.svg"))
            self.pushButton_max_and_reduction.setIcon(icon)
        else:
            self.showMaximized()
            self.pushButton_max_and_reduction.setMinimumSize(48, 44)
            self.pushButton_max_and_reduction.setToolTip("恢复")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/images/icon/minimize_2_reduce_icon.svg"))
            self.pushButton_max_and_reduction.setIcon(icon)

    '''以下三个方法用于实现鼠标拖动窗口和改变窗口大小'''

    # 重写鼠标点击事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.left_button_clicked = True  # 开启鼠标左键点击标志
            if event.pos() in self._top_rect:
                # 鼠标左键点击上侧边界区域
                self._top_drag = True
                event.accept()
            elif event.pos() in self._bottom_rect:
                # 鼠标左键点击下侧边界区域
                self._bottom_drag = True
                event.accept()
            elif event.pos() in self._left_rect:
                # 鼠标左键点击左侧边界区域
                self._left_drag = True
                event.accept()
            elif event.pos() in self._right_rect:
                # 鼠标左键点击右侧边界区域
                self._right_drag = True
                event.accept()
            elif event.pos() in self._left_top_rect:
                # 鼠标左键点击左上角边界区域
                self._left_top_drag = True
                event.accept()
            elif event.pos() in self._right_bottom_rect:
                # 鼠标左键点击右下角边界区域
                self._right_bottom_drag = True
                event.accept()
            elif event.pos() in self._right_top_rect:
                # 鼠标左键点击右上角边界区域
                self._right_top_drag = True
                event.accept()
            elif event.pos() in self._left_bottom_rect:
                # 鼠标左键点击左下角边界区域
                self._left_bottom_drag = True
                event.accept()
            elif event.y() < self.frame_menu.height():
                # 鼠标左键点击标题栏区域
                self._move_drag = True
                self.move_DragPosition = event.globalPos() - self.pos()
                event.accept()

    # 鼠标点击释放事件
    def mouseReleaseEvent(self, event):
        # 恢复为箭头鼠标样式
        self.setCursor(Qt.ArrowCursor)
        if event.button() == Qt.LeftButton:
            # 鼠标释放后各扳机复位
            self.left_button_clicked = False

            self._top_drag = False
            self._bottom_drag = False
            self._left_drag = False
            self._right_drag = False
            self._left_top_drag = False
            self._right_top_drag = False
            self._left_bottom_drag = False
            self._right_bottom_drag = False

            self._move_drag = False
        event.accept()

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        # x, y = event.x(), event.y()
        # child_widget = self.childAt(x, y)
        # if child_widget is None:
        #     print("No child widget at ({}, {})".format(x, y))
        # else:
        #     print("Child widget at ({}, {}): {}".format(x, y, child_widget))
        # 鼠标没点击时，根据光标位置设置光标样式
        if not self.left_button_clicked:
            self._set_cursor(event.pos())
        # 调整窗口大小
        if Qt.LeftButton:
            if self._left_drag:
                # 左侧调整窗口宽度
                new_width = self.width() + (self.x() - event.globalPos().x())
                if new_width >= self.minimumWidth():
                    self.setGeometry(event.globalPos().x(), self.y(), new_width, self.height())
                event.accept()
            elif self._top_drag:
                # 顶部调整窗口高度
                new_height = self.height() + (self.y() - event.globalPos().y())
                if new_height >= self.minimumHeight():
                    self.setGeometry(self.x(), event.globalPos().y(), self.width(), new_height)
                event.accept()
            elif self._left_top_drag:
                # 左上角调整窗口大小
                new_width = self.width() + (self.x() - event.globalPos().x())
                new_height = self.height() + (self.y() - event.globalPos().y())
                if new_width >= self.minimumWidth() and new_height >= self.minimumHeight():
                    self.setGeometry(event.globalPos().x(), event.globalPos().y(), new_width, new_height)
                event.accept()
            elif self._right_top_drag:
                # 右上角调整窗口大小
                new_width = event.globalPos().x() - self.x()
                new_height = self.height() + (self.y() - event.globalPos().y())
                if new_width >= self.minimumWidth() and new_height >= self.minimumHeight():
                    self.setGeometry(self.x(), event.globalPos().y(), new_width, new_height)
                event.accept()
            elif self._left_bottom_drag:
                # 左下角调整窗口大小
                new_width = self.width() + (self.x() - event.globalPos().x())
                new_height = event.globalPos().y() - self.y()
                if new_width >= self.minimumWidth() and new_height >= self.minimumHeight():
                    self.setGeometry(event.globalPos().x(), self.y(), new_width, new_height)
                event.accept()
            # 仅对于右下的方向，可以用resize实现，更平滑
            elif self._right_drag:
                # 右侧调整窗口宽度
                self.resize(event.pos().x(), self.height())
                event.accept()
            elif self._bottom_drag:
                # 底部调整窗口高度
                self.resize(self.width(), event.pos().y())
                event.accept()
            elif self._right_bottom_drag:
                # 右下角同时调整高度和宽度
                self.resize(event.pos().x(), event.pos().y())
                event.accept()
            elif self._move_drag:
                # 标题栏拖动窗口
                self.move(event.globalPos() - self.move_DragPosition)
                event.accept()

    # 根据光标位置设置光标形状
    def _set_cursor(self, point):
        if point in self._left_rect:
            # 左侧边界
            self.setCursor(Qt.SizeHorCursor)
        elif point in self._right_rect:
            # 右侧边界
            self.setCursor(Qt.SizeHorCursor)
        elif point in self._bottom_rect:
            # 底下边界
            self.setCursor(Qt.SizeVerCursor)
        elif point in self._top_rect:
            # 顶部边界
            self.setCursor(Qt.SizeVerCursor)
        elif point in self._left_top_rect:
            # 左上角边界
            self.setCursor(Qt.SizeFDiagCursor)
        elif point in self._left_bottom_rect:
            # 左下角边界
            self.setCursor(Qt.SizeBDiagCursor)
        elif point in self._right_top_rect:
            # 右上角边界
            self.setCursor(Qt.SizeBDiagCursor)
        elif point in self._right_bottom_rect:
            # 右下角边界
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
