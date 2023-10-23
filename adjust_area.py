from PyQt5.QtWidgets import QWidget

from widget_adjust_area import Ui_Form


class AdjustArea(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 设置ui