from PyQt5.QtWidgets import QWidget, QColorDialog, QFontDialog

from ui_py.widget_function_stack import Ui_Form


class FunctionStack(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 设置ui
