import cv2
import dlib
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import QLabel, QMessageBox

from tools.face_detect import FaceDetect
from tools.image_format import ImageFormat


# 该线程用来人脸检测
class Worker(QThread):
    image = pyqtSignal(object)

    def __init__(self, cv_image):
        super().__init__()
        self.cv_image = cv_image

    def run(self):
        detected_faces, cv_image = FaceDetect.detect(self.cv_image)
        self.image.emit((detected_faces, cv_image))


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

        # # 使用dlib的人脸检测器
        # detector = dlib.get_frontal_face_detector()
        # # 使用dlib的人脸关键点检测器
        # predictor = dlib.shape_predictor("tools/shape_predictor_68_face_landmarks.dat")
        #
        # # 将图像转换为灰度图
        # gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        # faces = detector(gray)
        # detected_faces = 0
        # for face in faces:
        #     print(face)
        #     # 检测关键点
        #     landmarks = predictor(gray, face)
        #
        #     # 绘制关键点
        #     for i in range(0, 67):
        #         x, y = landmarks.part(i).x, landmarks.part(i).y
        #         cv2.circle(cv_image, (x, y), 2, (0, 255, 0), -1)
        #
        #     detected_faces += 1
        # cv2.imshow(winname="human face test", mat=cv_image)


        # 开一个线程进行人脸检测
        if self.worker is None or not self.worker.isRunning():
            self.worker = Worker(cv_image)
            self.worker.image.connect(self.display_image)
            self.worker.start()

    # 转为QPixmap格式显示
    def display_image(self, result):
        detected_faces, cv_image = result
        pixmap = ImageFormat.cv_to_pixmap(cv_image)
        self.face_num.emit(detected_faces)
        self.setPixmap(pixmap)





# import cv2
# from PyQt5.QtCore import QTimer, QThread, pyqtSignal
# from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
# from tools.face_detect import FaceDetect
# from tools.image_format import ImageFormat
#
#
# class Camera(QLabel):
#     def __init__(self):
#         super().__init__()
#         self.setFixedSize(640, 480)
#         self.worker = Worker()
#         self.worker.pixmap.connect(self.setPixmap)
#         # self.worker.exit()
#
#     def open_camera(self):
#         if not self.worker.isRunning():
#             self.worker.start()
#
#     def close_camera(self):
#         print(self.worker.isRunning())
#         if self.worker.isRunning():
#             self.worker.terminate()
#
#
# class Worker(QThread):
#     pixmap = pyqtSignal(QPixmap)
#     face_num = pyqtSignal(int)
#
#     def __init__(self):
#         super().__init__()
#
#     def run(self):
#         capture = cv2.VideoCapture(0)
#         while True:
#             _, cv_image = capture.read()  # 从视频流中读取
#             cv_image = cv2.flip(cv_image, flipCode=1)  # 镜像显示
#             detected_faces, cv_image = FaceDetect.detect(cv_image)  # 人脸检测
#             self.pixmap.emit(ImageFormat.cv_to_pixmap(cv_image))
#             self.face_num.emit(detected_faces)

# import cv2
# import dlib
# from math import sqrt
# # Load the detector
# detector = dlib.get_frontal_face_detector()
#
# # Load the predictor
# predictor = dlib.shape_predictor("tools/shape_predictor_68_face_landmarks.dat")
#
# # read the image
# cap = cv2.VideoCapture(0)
#
# while True:
#     _, frame = cap.read()
#     # Convert image into grayscale
#     frame = cv2.flip(frame, flipCode=1)
#     gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)
#
#     # Use detector to find landmarks
#     faces = detector(gray)
#     print(faces)
#
#     for face in faces:
#         x1 = face.left()  # left point
#         y1 = face.top()  # top point
#         x2 = face.right()  # right point
#         y2 = face.bottom()  # bottom point
#
#         landmarks = predictor(image=gray, box=face)
#
#         # Loop through all the points
#         #for n in range(0, 68):
#         x67 = landmarks.part(67).x
#         y67 = landmarks.part(67).y
#         for n in range(0, 67):
#             x = landmarks.part(n).x
#             y = landmarks.part(n).y
#             x2 = landmarks.part(n+1).x
#             y2 = landmarks.part(n+1).y
#             ptStart=(x,y)
#             ptEnd=(x2,y2)
#             point_color=(0,255,0)
#             thickness=1
#             lineType=4
#             cv2.circle(img=frame, center=(x, y), radius=2, color=(0, 255, 0), thickness=-1)
#             if(n==16 or n==26 or n==35 or n==41 or n==47):
#                 continue
#             cv2.line(frame, ptStart, ptEnd, point_color, thickness, lineType)
#
#     cv2.imshow(winname="human face test", mat=frame)
#
#     if cv2.waitKey(delay=1) == 27:
#         break
#
# cap.release()
#
# cv2.destroyAllWindows()


# import numpy as np
# import cv2
# import dlib
#
# cap = cv2.VideoCapture(0)
# detector = dlib.get_frontal_face_detector()  # 创建一个容器
# predictor = dlib.shape_predictor("tools/shape_predictor_68_face_landmarks.dat")  # 加载一个自带的分类器
# while cap.isOpened():
#     success, img = cap.read()
#     if not success:
#         print("camera frame is empty!")
#         continue
#
#     img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 使图片转化为灰度图片
#     person = detector(img_grey, 0)  # 返回信息
#     for i in range(len(person)):
#         landmarks = np.matrix([[p.x, p.y] for p in predictor(img_grey, person[i]).parts()])  # 获取点的坐标
#         for idx, point in enumerate(landmarks):
#             pos = (point[0, 0], point[0, 1])
#             cv2.circle(img, pos, 2, (0, 0, 255), 2)  # 画圈圈，（255,0,0）是圈圈的颜色
#             # font = cv2.FONT_HERSHEY_SIMPLEX
#             # cv2.putText(img, str(idx + 1), pos, font, 0.3, (0, 0, 255), 1, cv2.LINE_AA)  # 为圈圈标上序号
#     cv2.imshow("img", img)  # 展示
#     if cv2.waitKey(10) & 0xFF == 27:
#         break
# cv2.destroyAllWindows()
# cap.release()


# import cv2
# from PyQt5.QtCore import QTimer
# from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
# from tools.face_detect import FaceDetect
# from tools.image_format import ImageFormat
#
#
# class Camera(QLabel):
#     def __init__(self):
#         super().__init__()
#         self.timer_camera = QTimer()  # 定义定时器，用于控制显示视频的帧率
#         self.cap = cv2.VideoCapture()  # 视频流
#         self.CAM_NUM = 0  # 为0时表示视频流来自默认摄像头
#         self.setFixedSize(640, 480)
#
#         self.timer_camera.timeout.connect(self.show_camera)  # 定时器结束，调用show_camera()
#
#     def open_camera(self):
#         if self.timer_camera.isActive() is False:  # 若定时器未启动
#             # 参数是0，打开笔记本的内置摄像头，参数是视频文件路径则打开视频
#             if self.cap.open(self.CAM_NUM) is False:  # open不成功
#                 QMessageBox.warning(self, 'warning', "请检查摄像头是否正确连接", buttons=QMessageBox.Ok)
#             else:
#                 self.timer_camera.start(30)  # 定时器计时30ms，每过30ms从摄像头中取一帧显示
#
#     def close_camera(self):
#         if self.timer_camera.isActive() is True:  # 若定时器已启动
#             self.timer_camera.stop()  # 关闭定时器
#             self.cap.release()  # 释放视频流
#             self.clear()  # 清空视频显示区域
#
#     def show_camera(self):
#         _, cv_image = self.cap.read()  # 从视频流中读取
#         cv_image = cv2.resize(cv_image, (640, 480))  # 读到的帧的大小重新设置为 640x480
#         cv_image = cv2.flip(cv_image, flipCode=1)  # 镜像显示
#         #detected_faces, cv_image = FaceDetect.detect(cv_image)  # 人脸检测
#         self.setPixmap(ImageFormat.cv_to_pixmap(cv_image))  # 转为QPixmap格式显示
