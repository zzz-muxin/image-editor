import cv2
import dlib
import numpy as np
from PIL import ImageEnhance, Image, ImageFilter
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from PyQt5.QtGui import QPixmap, QImage, QPainter
from scipy.interpolate import CubicSpline

from tools.image_format import ImageFormat


class FaceDetect(QThread):
    image_updated = pyqtSignal(QPixmap)  # 图片更新信号
    face_num = pyqtSignal(int)  # 人脸数量信号

    def __init__(self, pixmap: QPixmap):
        super().__init__()
        self.pixmap = pixmap
        self.cv_draw_pixmap = pixmap
        self.detect_face_num = 0

    # 使用opencv的模型进行人脸检测
    @staticmethod
    def cv_face_detect(image):
        # 加载预训练的模型, 使用TensorFlow深度学习框架
        # Tensorflow 的配置网络和训练的权重参数，model: .pb 文件，config: .pbtxt 文件
        # UINT8 是 TensorFlow 实现的 8 位量化版本
        net = cv2.dnn.readNetFromTensorflow("tools/opencv_face_detector_uint8.pb",
                                            "tools/opencv_face_detector.pbtxt")
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
        faces = []
        # 迭代所有检测结果
        for i in range(0, detections.shape[2]):
            # 获取当前检测结果的置信度
            confidence = detections[0, 0, i, 2]
            # 如果置信大于最小置信度，则将其可视化
            if confidence > 0.7:
                detected_faces += 1
                # 获取当前检测结果的坐标
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype('int')
                # 存储人脸坐标
                faces.append((startX, startY, endX, endY))
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
        return detected_faces, image, faces  # 返回值分别是检测到的人脸数量、绘制的检测结果图片、人脸矩形坐标信息列表

    # 人脸特征点识别
    @staticmethod
    def detect_landmarks(image):
        image = image.astype(np.uint8)
        # 使用dlib的人脸检测器
        detector = dlib.get_frontal_face_detector()
        # 使用dlib的68个人脸关键点检测器 + 新增的13个前额关键点
        predictor = dlib.shape_predictor("tools/shape_predictor_81_face_landmarks.dat")
        # 将图像转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 检测人脸
        faces = detector(gray)
        detected_faces = 0
        landmarks_list = []
        for face in faces:
            # 检测关键点
            landmarks = predictor(gray, face)
            landmarks_list.append(landmarks)
            # 绘制关键点
            for i in range(0, 81):
                x, y = landmarks.part(i).x, landmarks.part(i).y
                cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
            detected_faces += 1
        return detected_faces, image, landmarks_list  # 返回值分别是检测到的人脸数量、绘制的检测结果图片、人脸关键点列表

    # 设置图像
    def set_pixmap(self, pixmap: QPixmap):
        self.pixmap = pixmap

    # 返回绘制的图像
    def draw_face_img(self, cv_draw: bool):
        if cv_draw:
            self.image_updated.emit(self.cv_draw_pixmap)
        else:
            self.image_updated.emit(self.pixmap)

    # 检测人脸
    def detect_face(self):
        # 图片转为 nparray 数组
        image = ImageFormat.pixmap_to_cv(self.pixmap)
        image = image[:, :, :3]
        face_num, cv_draw_img, _ = self.cv_face_detect(image)  # opencv检测人脸
        if face_num != 0:
            self.cv_draw_pixmap = ImageFormat.cv_to_pixmap(cv_draw_img)
        self.detect_face_num = face_num
        self.face_num.emit(face_num)  # 发射检测到人脸数量信号

    def image_face_smooth(self, value):
        if self.detect_face_num != 0:
            image = ImageFormat.pixmap_to_cv(self.pixmap)
            image = image[:, :, :3]
            # 人脸检测
            face_num, image_cv_draw, faces = FaceDetect.cv_face_detect(image)
            face_num, image_dlib_draw, landmarks_list = FaceDetect.detect_landmarks(image)
            # 根据人脸特征点得到人脸区域掩膜
            face_mask = FaceDetect.face_mask(image, landmarks_list)
            # 对整张进行磨皮处理
            smoothed_img = FaceDetect.skin_smoothing(image, value)
            # 应用掩膜获取磨皮后的脸部图像
            smoothed_img = cv2.bitwise_and(smoothed_img, smoothed_img, mask=face_mask)
            # 将原始图像中的人脸区域替换为磨皮后的图像中的对应区域
            result_img = np.copy(image)
            result_img[face_mask > 0] = smoothed_img[face_mask > 0]
            # cv2.imshow('landmark', image_dlib_draw)
            # cv2.imshow('smooth_mask', smoothed_img)
            # cv2.imshow('result', result_img)
            if face_num == 0:
                new_pixmap = self.pixmap
            else:
                new_pixmap = ImageFormat.cv_to_pixmap(result_img)  # 更新图像
            self.image_updated.emit(new_pixmap)  # 发射图片更新信号
            self.face_num.emit(face_num)  # 发射检测到人脸数量信号

    # 磨皮算法
    @staticmethod
    def skin_smoothing(input_img, value):
        # 归一化到 [0, 1] 的范围
        input_img = np.array(input_img / 255.0, dtype=np.float32)
        # 曝光度调整为原图像的一半
        ea_img = input_img * pow(2, -1.0)
        # 绿色和蓝色通道叠加混合
        base = ea_img[..., 1]  # 提取绿色通道
        overlay = ea_img[..., 2]  # 提取蓝色通道
        ba = 2.0 * overlay * base  # 将蓝色通道的值乘以提取的绿色通道的值，并乘以 2
        ba_img = np.zeros((ba.shape[0], ba.shape[1], 3), dtype=np.float32)
        ba_img[..., 0] = ba
        ba_img[..., 1] = ba
        ba_img[..., 2] = ba
        # 进行高斯模糊
        radius = value  # int(np.ceil(7.0 * input_img.shape[0] / 750.0))  # 模糊半径为5时最理想
        # opencv的方法（效果不理想）
        # if(np.ceil(7.0*img.shape[0]/750.0)%2.0 == 0):
        #     radius = radius + 1
        # blur_img = cv2.GaussianBlur(ba_img,(99,99),0) #cv2.bilateralFilter(ba_img,radius,75,75)
        # PIL的方法
        pil_img = Image.fromarray(np.uint8(ba_img * 255.0))
        pil_blur = pil_img.filter(ImageFilter.GaussianBlur(radius))
        blur_img = np.asarray(pil_blur, np.float32) / 255.0
        # 进行高通滤波
        hp_img = ba_img - blur_img + 0.5  # 高反差保留
        # 生成高通滤波遮罩
        hard_light_color = hp_img[..., 2]
        [x1, y1] = np.where(hard_light_color < 0.5)
        [x2, y2] = np.where(hard_light_color >= 0.5)
        for i in range(3):
            # 3次强光处理，使噪声更加突出
            # 强调低亮度的区域
            hard_light_color[x1, y1] = hard_light_color[x1, y1] * hard_light_color[x1, y1] * 2.0
            # 增强对比度
            hard_light_color[x2, y2] = 1.0 - (1.0 - hard_light_color[x2, y2]) * (1.0 - hard_light_color[x2, y2]) * 2.0
        # 对结果进行缩放和剪切
        k = 255.0 / (164.0 - 75.0)
        hard_light_color = (hard_light_color - 75.0 / 255.0) * k
        hpass_img = np.zeros((hard_light_color.shape[0], hard_light_color.shape[1], 3))
        hpass_img[..., 0] = hard_light_color
        hpass_img[..., 1] = hard_light_color
        hpass_img[..., 2] = hard_light_color
        hpass_img = np.clip(hpass_img, 0, 1)
        # 曲线调色，增加亮度
        x = [0, 120.0 / 255.0, 1]
        y = [0, 146.0 / 255.0, 1]
        cs = CubicSpline(x, y)  # 利用锚点坐标生成三次样条曲线
        tc_img = cs(input_img)
        # 应用高通滤波遮罩到图像
        blend_img = input_img * hpass_img + tc_img * (1 - hpass_img)
        # 进行锐化突出细节
        enhancer = ImageEnhance.Sharpness(Image.fromarray(np.uint8(blend_img * 255.0)))
        img_sharp = enhancer.enhance(2)  # 锐化强度
        # 磨皮结果
        result = np.array(img_sharp, dtype=np.uint8)
        return result

    # 根据人脸关键点绘制掩膜
    @staticmethod
    def face_mask(input_img, faces_landmarks):
        mask = np.zeros_like(input_img[:, :, 0])  # 创建掩膜
        outline = list(range(0, 17))  # 面部区域关键点
        forehead = [78, 74, 79, 73, 72, 69, 68, 76, 75, 77]  # 前额区域关键点
        outline += forehead  # 合成整体脸部轮廓
        for landmarks in faces_landmarks:
            points = []  # 关键点坐标
            for i in outline:  # 人脸外围的关键点
                point = (landmarks.part(i).x, landmarks.part(i).y)
                points.append(point)
            # 将关键点转换为 NumPy 数组
            points = np.array(points, dtype=np.int32)
            points = points.reshape((-1, 1, 2))
            # 使用填充多边形函数创建掩膜
            cv2.fillPoly(mask, [points], 255)
        res = cv2.bitwise_and(input_img, input_img, mask=mask)
        # cv2.imshow('landmark', mask)
        # cv2.imshow('res', res)
        return mask

    # YCrCb椭圆肤色模型进行肤色检测(效果不理想，弃置)
    # @staticmethod
    # def YCrCb_ellipse_model(input_img):
    #     skinCrCbHist = np.zeros((256, 256), dtype=np.uint8)  # 创建一个256x256的二维数组
    #     cv2.ellipse(skinCrCbHist, (113, 155), (23, 25), 43, 0, 360, (255, 255, 255), -1)  # 绘制椭圆
    #     YCrCb = cv2.cvtColor(input_img, cv2.COLOR_BGR2YCR_CB)  # 转换至YCrCb空间
    #     # for face in faces:
    #     #     # 提取人脸区域坐标
    #     #     (startX, startY, endX, endY) = face
    #     #     # 在人脸区域应用肤色检测
    #     #     face_YCrCb = YCrCb[startY:endY, startX:endX, :]
    #     #     face_skin = np.zeros(face_YCrCb.shape[:2], dtype=np.uint8)
    #     #     for i in range(face_YCrCb.shape[0]):
    #     #         for j in range(face_YCrCb.shape[1]):
    #     #             if skinCrCbHist[face_YCrCb[i, j, 1], face_YCrCb[i, j, 2]] > 0:
    #     #                 face_skin[i, j] = 255
    #     #     # 将肤色检测结果放回原图
    #     #     YCrCb[startY:endY, startX:endX, 0] = cv2.bitwise_and(YCrCb[startY:endY, startX:endX, 0], face_skin)
    #     #     YCrCb[startY:endY, startX:endX, 1] = cv2.bitwise_and(YCrCb[startY:endY, startX:endX, 1], face_skin)
    #     #     YCrCb[startY:endY, startX:endX, 2] = cv2.bitwise_and(YCrCb[startY:endY, startX:endX, 2], face_skin)
    #     (Y, Cr, Cb) = cv2.split(YCrCb)  # 拆分出Y,Cr,Cb值
    #     skin_mask = np.zeros(Cr.shape, dtype=np.uint8)  # 掩膜
    #     (x, y) = Cr.shape
    #     for i in range(0, x):
    #         for j in range(0, y):
    #             if skinCrCbHist[Cr[i][j], Cb[i][j]] > 0:  # 若不在椭圆区间中
    #                 skin_mask[i][j] = 255
    #     res = cv2.bitwise_and(input_img, input_img, mask=skin_mask)
    #     #cv2.imshow('mask', skin_mask)
    #     # cv2.imshow('apply_mask', res)
    #     return skin_mask, res





