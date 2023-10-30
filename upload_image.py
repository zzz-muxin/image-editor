from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QFileDialog

from ui_py.widget_upload_image import Ui_Form


class UploadImageWidget(QWidget, Ui_Form):
    image_exist = pyqtSignal(QPixmap)  # 上传图片时传递信号

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 设置ui
        self.setAcceptDrops(True)  # 设置允许拖放文件
        self.pixmap = None

    # 重写鼠标点击事件，实现点击上传图片
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getOpenFileName(self, "选择图片文件", "",
                                                       "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)",
                                                       options=options)
            if file_name:
                try:
                    self.pixmap = QPixmap(file_name)
                    self.image_exist.emit(self.pixmap)  # 发射信号，传递加载的图片
                    print("image size:", self.pixmap.width(), self.pixmap.height())
                except Exception as e:
                    print("Error:", e)

    # 重写拖拽进入事件处理函数
    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls() and len(mime_data.urls()) == 1:  # 仅接受拖拽一个文件
            url = mime_data.urls()[0]  # 获取拖拽的第一个URL
            if url.isLocalFile() and url.toLocalFile().lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                # 改变样式
                self.widget_upload.setStyleSheet(".QWidget#widget_upload{\n"
                                                 "    border: 5px dashed #ccc;\n"
                                                 "    border-radius:10px;\n"
                                                 "    background-color:rgba(0, 170, 255, 50);\n"
                                                 "}\n")
                event.acceptProposedAction()

    # 重写拖拽离开事件处理函数
    def dragLeaveEvent(self, event):
        # 恢复样式
        self.widget_upload.setStyleSheet(".QWidget#widget_upload{\n"
                                         "    border: 5px dashed #ccc;\n"
                                         "    border-radius:10px;\n"
                                         "    background-color:transparent;\n"
                                         "}\n"
                                         ".QWidget#widget_upload:hover{\n"
                                         "    background-color: rgba(0, 170, 255, 50);\n"
                                         "}")

    # 重写拖放事件处理函数
    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls() and len(mime_data.urls()) == 1:
            url = mime_data.urls()[0]
            file_name = url.toLocalFile()
            try:
                pixmap = QPixmap(file_name)
                self.pixmap = pixmap
                self.image_exist.emit(pixmap)  # 发射信号，传递加载的图片
                print("image size:", pixmap.width(), pixmap.height())
            except Exception as e:
                print("Error:", e)
