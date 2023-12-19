import re

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtChart import QChartView
from PyQt5.QtCore import Qt, QPoint, QFileInfo
from PyQt5.QtGui import QColor, QEnterEvent, QPainter
from PyQt5.QtWidgets import QMainWindow, QGraphicsPixmapItem, QFileDialog, QMessageBox, QColorDialog, QFontDialog

from adjust_area import AdjustArea
from crop_box import CropBox
from function_stack import FunctionStack
from graphics_view import GraphicsView
from tools.adjust import Adjust
from tools.crop import Crop
from tools.flip import Flip
from tools.rotate import Rotate
from ui_py.main_window import Ui_MainWindow
from upload_image import UploadImageWidget
from chart_area import ChartArea
from tools.histogram import GrayChart, RGBChart
from face_area import FaceArea
from tools.face_detect import FaceDetect
from tools.switch_button import SwitchButton
from tools.curve import Curve
from tools.text import Text
from tools.camera import Camera


# from function_bar import FunctionBar


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
        self.curve_chart = None
        self.gray_chart = None
        self.rgb_chart = None
        self.face_detect = None
        self.camera = None
        self.rotate = Rotate()
        self.adjust = Adjust()
        self._init_all_widget()  # 初始化所有组件的事件

    # 初始化所有组件的事件
    def _init_all_widget(self):
        self.function_stack = FunctionStack()
        self.adjust_area = AdjustArea()
        self.chart_area = ChartArea()
        self.face_area = FaceArea()
        self.pushButton_home.clicked.connect(self.press_button_home)  # 主页按钮
        self.pushButton_zoom_in.clicked.connect(self.press_button_zoom_in)  # 放大按钮
        self.pushButton_zoom_out.clicked.connect(self.press_button_zoom_out)  # 缩小按钮
        self.pushButton_save.clicked.connect(self.save_image)  # 保存按钮
        self.pushButton_crop.clicked.connect(self.press_button_crop)  # 裁剪按钮
        self.pushButton_rotate.clicked.connect(self.press_button_rotate)  # 旋转按钮
        self.pushButton_chart.clicked.connect(self.press_button_chart)  # 图表按钮
        self.pushButton_adjust.clicked.connect(self.press_button_adjust)  # 调整区域按钮
        self.pushButton_face.clicked.connect(self.press_button_face)  # 人脸按钮
        self.pushButton_text.clicked.connect(self.press_button_text)  # 文字按钮
        self.function_stack.slider_rotate.valueChanged.connect(self.slider_rotate)  # 滑动条旋转
        self.function_stack.pushButton_right_90.clicked.connect(self.rotate_90_clockwise)  # 顺时针旋转
        self.function_stack.pushButton_left_90.clicked.connect(self.rotate_90_counterclockwise)  # 逆时针旋转
        self.function_stack.pushButton_flip_x.clicked.connect(self.flip_x)  # 水平镜像
        self.function_stack.pushButton_flip_y.clicked.connect(self.flip_y)  # 垂直镜像
        self.function_stack.pushButton_text_color.clicked.connect(self.show_color_dialog)  # 字体颜色按钮
        self.function_stack.pushButton_font.clicked.connect(self.show_font_dialog)  # 字体按钮
        self.function_stack.pushButton_cancel_text.clicked.connect(self.cancel_text)  # 取消字体按钮
        self.function_stack.pushButton_apply_text.clicked.connect(self.apply_text)  # 应用字体按钮
        self.adjust_area.slider_saturation.valueChanged.connect(self.saturation_adjust)
        self.adjust_area.slider_contrast.valueChanged.connect(self.contrast_adjust)
        self.adjust_area.slider_brightness.valueChanged.connect(self.brightness_adjust)

        uploader = UploadImageWidget()
        self.horizontalLayout_upload.addWidget(uploader)  # 添加自定义的上传图片UploadImageWidget类
        uploader.image_exist.connect(self.init_image_widget)  # 初始化与图片相关的组件

        # 一个垂直布局套一个水平布局
        self.horizontalLayout_view = QtWidgets.QHBoxLayout()
        self.horizontalLayout_view.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_view.setObjectName("horizontalLayout_view")
        self.verticalLayout_image_view = QtWidgets.QVBoxLayout()
        self.verticalLayout_image_view.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_image_view.setObjectName("verticalLayout_image_view")
        self.verticalLayout_image_view.addLayout(self.horizontalLayout_view)
        self.verticalLayout_image_view.setStretch(0, 1)
        self.verticalLayout_image_view.addWidget(self.function_stack)
        self.function_stack.hide()

    # 初始化与图片相关的组件
    def init_image_widget(self, pixmap):
        self.graphicsView = GraphicsView(pixmap, self)  # 查看图片的GraphicsView
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭垂直滑动条
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭水平滑动条
        self.page_image_view.setLayout(self.verticalLayout_image_view)  # 设置垂直布局

        self.horizontalLayout_view.addWidget(self.chart_area)
        self.horizontalLayout_view.setStretch(0, 1)
        self.chart_area.hide()

        self.horizontalLayout_view.addWidget(self.graphicsView)  # 添加graphicsView到布局
        self.horizontalLayout_view.setStretch(1, 2)

        self.horizontalLayout_view.addWidget(self.adjust_area)
        self.horizontalLayout_view.setStretch(2, 1)
        self.adjust_area.hide()

        self.horizontalLayout_view.addWidget(self.face_area)
        self.horizontalLayout_view.setStretch(3, 1)
        self.face_area.hide()

        # 曲线调色
        self.curve_chart = Curve(pixmap)
        self.curve_chart.image_updated.connect(self.pixmap_update)
        self.chart_area.verticalLayout_curve.addWidget(self.curve_chart)
        # 连接按钮信号
        self.chart_area.pushButton_colorful.clicked.connect(self.press_colorful_button)
        self.chart_area.pushButton_red.clicked.connect(self.press_red_button)
        self.chart_area.pushButton_green.clicked.connect(self.press_green_button)
        self.chart_area.pushButton_blue.clicked.connect(self.press_blue_button)
        # 灰度直方图
        self.gray_chart = GrayChart(pixmap)
        self.chart_area.verticalLayout_gray_hist.addWidget(self.gray_chart)
        # rgb直方图
        self.rgb_chart = RGBChart(pixmap)
        self.chart_area.verticalLayout_rgb_hist.addWidget(self.rgb_chart)
        # 连接直方图均衡化信号
        self.rgb_chart.image_updated.connect(self.pixmap_update)
        self.rgb_chart.image_updated.connect(self.gray_chart.set_pixmap)
        self.chart_area.switch_button.clickedOn.connect(self.rgb_chart.hist_equalize)
        self.chart_area.switch_button.clickedOff.connect(self.rgb_chart.hist_restore)

        # 字体spinBox信号
        self.function_stack.spinBox.valueChanged.connect(self.graphicsView.spinbox_change)

        # 人脸检测
        self.face_detect = FaceDetect(pixmap)
        self.face_detect.image_updated.connect(self.pixmap_update)
        self.face_detect.face_num.connect(self.face_area.label_face_num.setNum)
        self.face_area.switch_button.clickedOn.connect(self.open_camera)
        self.face_area.switch_button.clickedOff.connect(self.close_camera)

        self.adjust.set_pixmap(pixmap)
        self.graphicsView.scale_signal.connect(self.show_label_scale)  # 连接到图片缩放比例显示方法

        self.main_stacked_widget.setCurrentIndex(1)  # 跳转到图片视图界面

    # 图片缩放比例显示
    def show_label_scale(self, scale):
        self.label_scale.setText(f"{scale * 100: .1f}%")  # 用f-string格式化输出

    # 通过滑动条旋转
    def slider_rotate(self, degree):
        pixmap_item = self.graphicsView.pixmap_item
        self.function_stack.label_rotate.setText(f"{degree}°")  # 显示旋转角度
        pixmap_item.setTransformOriginPoint(pixmap_item.pixmap().width() / 2, pixmap_item.pixmap().height() / 2)
        pixmap_item.setRotation(degree)
        # pixmap = self.rotate.rotate_by_slider(degree)
        # self.graphicsView.pixmap_item.setPixmap(pixmap)

    # 顺时针旋转90度
    def rotate_90_clockwise(self):
        pixmap = Rotate.rotate(self.graphicsView.get_pixmap(), 90)
        self.graphicsView.set_pixmap(pixmap)

    # 逆时针旋转90度
    def rotate_90_counterclockwise(self):
        pixmap = Rotate.rotate(self.graphicsView.get_pixmap(), -90)
        self.graphicsView.set_pixmap(pixmap)

    # 水平镜像
    def flip_x(self):
        pixmap = Flip.flip_x(self.graphicsView.get_pixmap())
        self.graphicsView.set_pixmap(pixmap)

    # 垂直镜像
    def flip_y(self):
        pixmap = Flip.flip_y(self.graphicsView.get_pixmap())
        self.graphicsView.set_pixmap(pixmap)

    # 饱和度
    def saturation_adjust(self, value):
        pixmap = self.adjust.adjust_saturation(value)
        self.graphicsView.set_pixmap(pixmap)

    def contrast_adjust(self, value):
        pixmap = self.adjust.adjust_contrast(value)
        self.graphicsView.set_pixmap(pixmap)

    def brightness_adjust(self, value):
        pixmap = self.adjust.adjust_brightness(value)
        self.graphicsView.set_pixmap(pixmap)

    # 检查graphicsView视图内是否存在图元
    def is_pixmap_exist(self):
        if self.graphicsView is not None:
            for item in self.graphicsView.items():
                if isinstance(item, QGraphicsPixmapItem):
                    return True
        return False

    # 主页按钮
    def press_button_home(self):
        self.main_stacked_widget.setCurrentIndex(0)

    # 放大视图
    def press_button_zoom_in(self):
        if self.is_pixmap_exist():
            self.graphicsView.zoom_in_view()

    # 缩小视图
    def press_button_zoom_out(self):
        if self.is_pixmap_exist():
            self.graphicsView.zoom_out_view()

    # 图表按钮
    def press_button_chart(self):
        if self.is_pixmap_exist():
            self.main_stacked_widget.setCurrentIndex(1)
            self.curve_chart.set_pixmap(self.graphicsView.get_pixmap())
            self.gray_chart.set_pixmap(self.graphicsView.get_pixmap())
            self.rgb_chart.set_pixmap(self.graphicsView.get_pixmap())
            self.chart_area.show()
            self.adjust_area.hide()
            self.function_stack.hide()
            self.face_area.hide()

    # 点击彩色按钮
    def press_colorful_button(self):
        self.curve_chart.click_colorful_button()

    # 点击红色按钮
    def press_red_button(self):
        self.curve_chart.click_red_button()

    # 点击绿色按钮
    def press_green_button(self):
        self.curve_chart.click_green_button()

    # 点击蓝色按钮
    def press_blue_button(self):
        self.curve_chart.click_blue_button()

    # 更新视图的图片
    def pixmap_update(self, pixmap):
        self.graphicsView.set_pixmap(pixmap)

    # 人脸按钮
    def press_button_face(self):
        if self.is_pixmap_exist():
            self.face_detect.image_detect()
            self.main_stacked_widget.setCurrentIndex(1)
            self.face_area.show()
            self.adjust_area.hide()
            self.chart_area.hide()
            self.function_stack.hide()

    # 打开摄像头
    def open_camera(self):
        if self.camera is None:
            self.camera = Camera()
            # self.camera.face_num.connect(self.face_area.label_face_num.setNum)
            self.graphicsView.scene.addWidget(self.camera)
        self.camera.open_camera()
        self.camera.show()
        self.graphicsView.pixmap_item.hide()

    # 关闭摄像头
    def close_camera(self):
        self.camera.close_camera()
        self.face_detect.image_detect()
        self.camera.hide()
        self.graphicsView.pixmap_item.show()

    # 文本按钮
    def press_button_text(self):
        if self.is_pixmap_exist():
            self.main_stacked_widget.setCurrentIndex(1)  # 跳转到图片视图page
            self.function_stack.basic_function_stack.setCurrentIndex(2)  # 跳转到文字菜单栏
            self.adjust_area.hide()
            self.chart_area.hide()
            self.face_area.hide()
            self.function_stack.show()
            self.graphicsView.add_text_edit()  # 新增文本编辑框

    # 文字颜色按钮显示颜色对话框
    def show_color_dialog(self):
        # 保存当前颜色
        self.orig_color = self.get_current_color()
        # 创建颜色对话框
        color_dialog = QColorDialog()
        color_dialog.currentColorChanged.connect(self.preview_color)
        color_dialog.rejected.connect(self.cancel_select_color)
        color_dialog.exec_()

    # 预览文字颜色
    def preview_color(self, color):
        style_sheet = (
            f".QPushButton{{"
            f"background-color: {color.name()};"
            f"border-radius: 15px;"
            f"}}"
        )
        self.function_stack.pushButton_text_color.setStyleSheet(style_sheet)
        self.graphicsView.change_text_color(color)

    # 取消选择颜色
    def cancel_select_color(self):
        style_sheet = (
            f".QPushButton{{"
            f"background-color: {self.orig_color.name()};"
            f"border-radius: 15px;"
            f"}}"
        )
        self.function_stack.pushButton_text_color.setStyleSheet(style_sheet)
        self.graphicsView.change_text_color(self.orig_color)

    # 获取当前pushButton_text_color颜色
    def get_current_color(self):
        # 使用正则表达式提取 background-color 的值
        match = re.search(r"background-color:\s*([^;]+);",
                          self.function_stack.pushButton_text_color.styleSheet())
        if match:
            background_color = match.group(1)
            return QColor(background_color)

    # 显示字体对话框
    def show_font_dialog(self):
        font_dialog = QFontDialog()
        font_dialog.currentFontChanged.connect(self.graphicsView.change_text_font)
        font_dialog.exec_()

    # 取消文本按钮
    def cancel_text(self):
        self.main_stacked_widget.setCurrentIndex(1)  # 跳转到图片视图page
        self.function_stack.hide()
        self.graphicsView.delete_text()  # 删除所有文本

    # 应用文本按钮
    def apply_text(self):
        #self.function_stack.hide()
        self.graphicsView.draw_text()  # 绘制文本
        self.graphicsView.delete_text()  # 删除所有文本

    # 调节按钮
    def press_button_adjust(self):
        if self.is_pixmap_exist():
            # 存在图片才显示adjust_area
            self.main_stacked_widget.setCurrentIndex(1)
            self.adjust_area.show()
            self.chart_area.hide()
            self.function_stack.hide()
            self.face_area.hide()

    # 旋转按钮
    def press_button_rotate(self):
        if self.is_pixmap_exist():
            self.rotate.set_pixmap(self.graphicsView.get_pixmap())  # 设置当前旋转图片
            self.main_stacked_widget.setCurrentIndex(1)
            self.function_stack.basic_function_stack.setCurrentIndex(1)
            self.adjust_area.hide()
            self.chart_area.hide()
            self.function_stack.show()
            self.face_area.hide()

    # 裁剪按钮
    def press_button_crop(self):
        crop_box_exist = False
        if self.is_pixmap_exist():
            self.main_stacked_widget.setCurrentIndex(1)  # 跳转到图片视图page
            self.function_stack.basic_function_stack.setCurrentIndex(0)  # 跳转到裁剪功能page
            self.adjust_area.hide()
            self.chart_area.hide()
            self.face_area.hide()
            self.function_stack.show()
            for item in self.graphicsView.items():
                if isinstance(item, CropBox):
                    # 检查graphicsView内是否已存在裁剪框
                    # self.graphicsView.show_crop_box()  # 显示裁剪框
                    crop_box_exist = True
            # 不存在裁剪框则新建
            if not crop_box_exist:
                self.graphicsView.add_crop_box()  # 新增裁剪框
                self.function_stack.pushButton_apply.clicked.connect(self.press_crop_apply)  # 应用裁剪按钮
                self.function_stack.pushButton_cancel.clicked.connect(self.press_crop_cancel)  # 取消裁剪按钮

    def press_crop_apply(self):
        if self.graphicsView.crop_box:
            pixmap = self.graphicsView.get_pixmap()
            rect = self.graphicsView.crop_box.parentRect()
            pixmap_cropped = Crop.crop_image(pixmap, rect)  # 参数为裁剪的图片和框选的范围
            self.graphicsView.set_pixmap(pixmap_cropped)  # 设置为裁剪后的图片
            self.graphicsView.pixmap_item.setPos(self.graphicsView.crop_box.getSceneTopLeft())  # 重新设置左上角点位
            self.graphicsView.crop_box.updateState()  # 裁剪后更新裁剪框状态

    def press_crop_cancel(self):
        self.graphicsView.delete_crop_box()  # 删除裁剪框
        self.function_stack.hide()

    # 保存图片
    def save_image(self):
        try:
            if self.is_pixmap_exist():
                # 弹出文件保存对话框
                options = QFileDialog.Options()
                file_name, _ = QFileDialog.getSaveFileName(self, "保存图片", "",
                                                           "Image Files (*.jpg *.jpeg *.png *.bmp);;All Files (*)",
                                                           options=options)
                if file_name:
                    try:
                        # 使用QPixmap的save方法保存图像
                        self.graphicsView.get_pixmap().save(file_name)
                    except Exception as e:
                        # 弹出保存失败的警告框
                        QMessageBox.warning(self, "保存失败", f"{e}", QMessageBox.Ok)
        except Exception as e:
            print(e)

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
