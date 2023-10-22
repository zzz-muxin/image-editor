from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QFileDialog

from widget_upload_image import Ui_Form


class UploadImage(QWidget, Ui_Form):
    image = pyqtSignal(QPixmap)  # 上传图片时传递信号

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
                    self.image.emit(self.pixmap)  # 发射信号，传递加载的图片
                    print("image size:", self.pixmap.width(), self.pixmap.height())
                except Exception as e:
                    print("Error:", e)

    # 重写拖拽进入事件处理函数
    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls() and len(mime_data.urls()) == 1:  # 仅接受拖拽一个文件
            url = mime_data.urls()[0]
            if url.isLocalFile() and url.toLocalFile().lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                event.acceptProposedAction()

    # 重写拖放事件处理函数
    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls() and len(mime_data.urls()) == 1:
            url = mime_data.urls()[0]
            file_name = url.toLocalFile()
            try:
                pixmap = QPixmap(file_name)
                self.pixmap = pixmap
                self.image.emit(pixmap)  # 发射信号，传递加载的图片
                print("image size:", pixmap.width(), pixmap.height())
            except Exception as e:
                print("Error:", e)

    # # 重写拖拽文件方法
    # def dragEnterEvent(self, event):
    #     # 当拖拽的文件拥有url则接受拖拽调用dropEvent
    #     if event.mineData().hasUrls():
    #         event.acceptProposedAction()
    #
    # def dropEvent(self, event):
    #     image_url = event.mimeData().urls()[0]  # 获取拖拽的第一个URL
    #     self.pixmap = QPixmap(image_url.toLocalFile())
    #     self.update()  # 重新绘制Widget以显示图片

    # def dragEnterEvent(self, event):
    #     if event.mimeData().hasUrls():
    #         event.acceptProposedAction()
    #
    # def dropEvent(self, event):
    #     image_url = event.mimeData().urls()[0]  # 获取拖拽的第一个URL
    #     pixmap = QPixmap(image_url.toLocalFile())
    #     if not pixmap.isNull():
    #         self.image = pixmap
    #         self.update()  # 重新绘制Widget以显示图片
    #
    # def paintEvent(self, event):
    #     if self.image:
    #         painter = QPainter(self)
    #         painter.drawPixmap(0, 0, self.image)
