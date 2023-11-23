import cv2
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import QLabel, QMessageBox

from tools.face_detect import FaceDetect
from tools.image_format import ImageFormat


# 该线程用来人脸检测
class Worker(QThread):
    image_processed = pyqtSignal(object)

    def __init__(self, cv_image):
        super().__init__()
        self.cv_image = cv_image

    def run(self):
        detected_faces, cv_image = FaceDetect.detect(self.cv_image)
        self.image_processed.emit((detected_faces, cv_image))


# 用QLabel来显示摄像头画面的Camera类
class Camera(QLabel):
    face_num = pyqtSignal(int)  # 人脸数量信号

    def __init__(self):
        super().__init__()
        self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.cap = cv2.VideoCapture()  # 视频流
        self.CAM_NUM = 0  # 为0时表示视频流来自默认摄像头
        self.setFixedSize(640, 480)

        self.worker = None

        self.timer_camera.timeout.connect(self.show_camera)  # 定时器结束，调用show_camera()

    def open_camera(self):
        # 若定时器未启动
        if not self.timer_camera.isActive():
            # 参数是0，打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if self.cap.open(self.CAM_NUM):
                self.timer_camera.start(30)  # 定时器计时30ms，每过30ms从摄像头中取一帧显示
            else:
                QMessageBox.warning(self, 'warning', "请检查摄像头是否正确连接", buttons=QMessageBox.Ok)

    def close_camera(self):
        # 若定时器已启动
        if self.timer_camera.isActive():
            self.timer_camera.stop()  # 关闭定时器
            self.cap.release()  # 释放视频流
            self.clear()  # 清空视频显示区域
            self.worker.quit()  # 结束人脸检测线程

    def show_camera(self):
        _, cv_image = self.cap.read()  # 从视频流中读取
        cv_image = cv2.resize(cv_image, (640, 480))  # 读到的帧的大小重新设置为 640x480
        cv_image = cv2.flip(cv_image, flipCode=1)  # 镜像显示

        # 开一个线程进行人脸检测
        if self.worker is None or not self.worker.isRunning():
            self.worker = Worker(cv_image)
            self.worker.image_processed.connect(self.display_image)
            self.worker.start()

    # 转为QPixmap格式显示
    def display_image(self, result):
        detected_faces, cv_image = result
        pixmap = ImageFormat.cv_to_pixmap(cv_image)
        self.face_num.emit(detected_faces)
        self.setPixmap(pixmap)
