
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap


class History:

    update_pixmap = pyqtSignal(QPixmap)

    def __init__(self):
        self.undo_stack = []  # 撤销的历史记录栈
        self.redo_stack = []  # 重做的历史记录栈

    def undo(self):
        if len(self.undo_stack) > 1:
            pixmap = self.undo_stack.pop()
            self.redo_stack.append(pixmap)
            self.update_pixmap.emit(pixmap)

    def redo(self):
        if len(self.redo_stack) > 0:
            pixmap = self.redo_stack.pop()
            self.undo_stack.append(pixmap)
            self.update_pixmap.emit(pixmap)
