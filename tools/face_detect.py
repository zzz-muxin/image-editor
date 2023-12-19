import cv2
import dlib
import numpy as np
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from PyQt5.QtGui import QPixmap
from tools.image_format import ImageFormat


class FaceDetect(QThread):
    image_updated = pyqtSignal(QPixmap)  # 图片更新信号
    face_num = pyqtSignal(int)  # 人脸数量信号

    def __init__(self, pixmap: QPixmap):
        super().__init__()
        self.pixmap = pixmap

    @staticmethod
    def detect(image):
        # # 使用dlib的人脸关键点检测器
        # predictor = dlib.shape_predictor("tools/shape_predictor_68_face_landmarks.dat")
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 加载预训练的模型, 使用TensorFlow深度学习框架
        # Tensorflow 的配置网络和训练的权重参数，model: .pb 文件，config: .pbtxt 文件
        net = cv2.dnn.readNetFromTensorflow("tools/opencv_face_detector_uint8.pb", "tools/opencv_face_detector.pbtxt")
        # 设置使用 CUDA 加速，需要从源码编译安装支持CUDA版本的opencv
        # net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        # net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        blob = cv2.dnn.blobFromImage(image,
                                     1.0,
                                     (300, 300),
                                     [0, 0, 0],
                                     False,
                                     False)
        # 将 blob 设置为输入并获取检测结果
        net.setInput(blob)
        detections = net.forward()

        detected_faces = 0
        w, h = image.shape[1], image.shape[0]
        # 迭代所有检测结果
        for i in range(0, detections.shape[2]):
            # 获取当前检测结果的置信度
            confidence = detections[0, 0, i, 2]
            # 如果置信大于最小置信度，则将其可视化
            if confidence > 0.5:
                detected_faces += 1
                # 获取当前检测结果的坐标
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype('int')
                # 绘制检测结果和置信度
                text = "{:.3f}%".format(confidence * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                print(detected_faces, confidence)
                image = image.astype(np.uint8)  # 改为uint8格式
                cv2.rectangle(image, (startX, startY), (endX, endY), (255, 0, 0), 3)
                cv2.putText(image,
                            text,
                            (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (0, 0, 255),
                            2)
        return detected_faces, image

    @staticmethod
    def detect_landmarks(image):
        image = image.astype(np.uint8)
        # 使用dlib的人脸检测器
        detector = dlib.get_frontal_face_detector()
        # 使用dlib的人脸关键点检测器
        predictor = dlib.shape_predictor("tools/shape_predictor_68_face_landmarks.dat")

        # 将图像转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 检测人脸
        faces = detector(gray)
        detected_faces = 0
        for face in faces:
            print(face)
            # 检测关键点
            landmarks = predictor(gray, face)

            # 绘制关键点
            for i in range(0, 68):
                x, y = landmarks.part(i).x, landmarks.part(i).y
                cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

            detected_faces += 1

        return detected_faces, image

    # @staticmethod
    def image_detect(self):
        image = ImageFormat.pixmap_to_cv(self.pixmap)
        image = image[:, :, :3]
        detected_faces, image = self.detect(image)
        if detected_faces == 0:
            new_pixmap = self.pixmap
        else:
            new_pixmap = ImageFormat.cv_to_pixmap(image)  # 更新图像
        self.image_updated.emit(new_pixmap)  # 发射图片更新信号
        self.face_num.emit(detected_faces)  # 发射检测到人脸数量信号


# class FaceDetect(QThread):
#     DetectOneFrame = pyqtSignal(QImage)
#
#     def __init__(self):
#         super().__init__()
#         self.working = None
#
#     def run(self):
#         face_cascade = cv2.CascadeClassifier('./static/cascade.xml')
#         capture = cv2.VideoCapture(0)
#         while self.working:
#             ret, frame_color = capture.read()
#             (height, width, channels) = frame_color.shape
#             frame_color = cv2.flip(frame_color, flipCode=1)  # 镜像
#             gray = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)
#             faces = face_cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=5, minSize=(5, 5))
#             for (x, y, w, h) in faces:
#                 cv2.rectangle(frame_color, (x, y), (x + w, y + w), (255, 255, 0), 4)
#             ui_image = QImage(cv2.cvtColor(frame_color, cv2.COLOR_BGR2RGB), width, height, QImage.Format_RGB888)
#             self.DetectOneFrame.emit(ui_image)
#         capture.release()
#         print('结束人脸检测')
