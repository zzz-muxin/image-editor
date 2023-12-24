import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from app import AppWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_win = AppWindow()
    app_win.setWindowTitle("image-editor")
    mainIcon = QIcon('images/icon/image_photo_picture_gallery_icon.png')
    app_win.setWindowIcon(mainIcon)
    app_win.show()
    sys.exit(app.exec_())
