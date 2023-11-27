from PyQt5.QtWidgets import QWidget

from tools.switch_button import SwitchButton
from ui_py.widget_chart_area import Ui_Form


class ChartArea(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 设置ui
        self.switch_button = SwitchButton()  # 直方图均衡化开关按钮
        self.horizontalLayout_switch.addWidget(self.switch_button)


