from PyQt5.QtWidgets import QWidget

from tools.switch_button import SwitchButton
from ui_py.widget_face_area import Ui_Form


class FaceArea(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 设置ui
        # 摄像头开关按钮
        self.switch_button_camera = SwitchButton()
        self.horizontalLayout_switch_camera.addWidget(self.switch_button_camera)
        # 人脸检测框开关按钮
        self.switch_button_rect = SwitchButton()
        self.horizontalLayout_switch_rect.addWidget(self.switch_button_rect)


