from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap


# 历史记录类
class History(QObject):
    image_updated = pyqtSignal(QPixmap)  # 图像更新信号
    undo_enable = pyqtSignal(bool)  # 是否可撤销
    redo_enable = pyqtSignal(bool)  # 是否可重做
    reset_enable = pyqtSignal(bool)  # 是否可重置

    def __init__(self, pixmap: QPixmap):
        super().__init__()
        self.orig_pixmap = pixmap  # 原始图像
        self.undo_stack = []  # 撤销的历史记录栈
        self.redo_stack = []  # 重做的历史记录栈
        self.undo_stack.append(self.orig_pixmap)  # 将原始图像添加到撤销栈栈底

    # 撤销
    def undo(self):
        if len(self.undo_stack) > 1:
            pixmap = self.undo_stack.pop()  # 将撤销的历史记录栈的栈顶图像出栈
            self.redo_stack.append(pixmap)  # 入栈重做的历史记录栈
            self.enable()
            last_pixmap = self.undo_stack[-1]  # 上一次的图像
            self.image_updated.emit(last_pixmap)  # 发射图像更新信号

    # 重做
    def redo(self):
        if len(self.redo_stack) > 0:
            pixmap = self.redo_stack.pop()  # 将重做的历史记录栈的栈顶图像出栈
            self.undo_stack.append(pixmap)  # 入栈撤销的历史记录栈
            self.enable()
            self.image_updated.emit(pixmap)  # 发射图像更新信号

    # 重置为初始图像
    def reset(self):
        # print("撤销栈", self.undo_stack)
        # print("重做栈", self.redo_stack)
        self.undo_stack.clear()  # 清空撤销栈
        self.redo_stack.clear()  # 清空重做栈
        self.undo_stack.append(self.orig_pixmap)  # 添加原始图像到撤销栈
        self.enable()
        self.image_updated.emit(self.orig_pixmap)  # 发射图像更新信号

    # 添加到撤销栈
    def undo_stack_append(self, pixmap: QPixmap):
        self.undo_stack.append(pixmap)
        self.enable()

    # 添加到重做栈
    def redo_stack_append(self, pixmap: QPixmap):
        self.redo_stack.append(pixmap)
        self.enable()

    # 检测是否可撤销、重做、重置
    def enable(self):
        if len(self.undo_stack) > 1:
            self.undo_enable.emit(True)
        else:
            self.undo_enable.emit(False)
        if len(self.redo_stack) > 0:
            self.redo_enable.emit(True)
        else:
            self.redo_enable.emit(False)
        if len(self.undo_stack) > 1 or len(self.redo_stack) > 0:
            self.reset_enable.emit(True)
        else:
            self.reset_enable.emit(False)

    # 设置原始图像
    def set_pixmap(self, pixmap: QPixmap):
        self.orig_pixmap = pixmap
