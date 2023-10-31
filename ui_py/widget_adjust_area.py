# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_xml/widget_adjust_area.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(331, 514)
        Form.setStyleSheet("background-color: transparent;;")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_adjust = QtWidgets.QWidget(Form)
        self.widget_adjust.setStyleSheet("QWidget{\n"
"    border-radius:20px;\n"
"    background-color: rgb(32, 32, 32);\n"
"}\n"
"QScrollBar:horizontal{\n"
"    height:8px;\n"
"    background:rgba(0,0,0,0%);\n"
"border-radius:4px;\n"
"\n"
"}\n"
"QScrollBar::handle:horizontal{\n"
"    background:rgba(255,255,255,50%);\n"
"border-radius:4px;\n"
"}\n"
"QScrollBar::handle:horizontal:hover{\n"
"    background:rgba(255,255,255,100%);\n"
"    min-width:0;\n"
"}\n"
"QScrollBar::add-line:horizontal{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::sub-line:horizontal{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::add-line:horizontal:hover{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::sub-line:horizontal:hover{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::add-page:horizontal,QScrollBar::sub-page:horizontal\n"
"{\n"
"    background:rgba(0,0,0,10%);\n"
"    border-radius:4px;\n"
"}\n"
"\n"
"QScrollBar:vertical{\n"
"    width:8px;\n"
"    background:rgba(0,0,0,0%);\n"
"\n"
"}\n"
"QScrollBar::handle:vertical{\n"
"    width:0px;\n"
"    background:rgba(255,255,255,50%);\n"
"    border-radius:4px;\n"
"}\n"
"QScrollBar::handle:vertical:hover{\n"
"    width:0px;\n"
"    background:rgba(255,255,255,100%);\n"
"    border-radius:4px;\n"
"    min-width:20;\n"
"}\n"
"QScrollBar::add-line:vertical{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::sub-line:vertical{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::add-line:vertical:hover{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::sub-line:vertical:hover{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical\n"
"{\n"
"    background:rgba(0,0,0,10%);\n"
"    border-radius:4px;\n"
"}\n"
"\n"
" \n"
" \n"
"QSlider::add-page:horizontal {\n"
"    background-color: qlineargradient(spread: pad, x1: 0, y1: 1, x2: 1, y2: 1,\n"
"                                      stop: 0 rgb(100, 100, 100),\n"
"                                      stop: 1 rgb(255, 78, 0,));\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background-color: qlineargradient(spread: pad, x1: 0, y1: 1, x2: 1, y2: 1,\n"
"                                      stop: 0 rgb(51, 151, 255),\n"
"                                      stop: 1 rgb(100, 100, 100));\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::groove:horizontal {\n"
"    background: transparent;\n"
"    height: 8px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    width: 16px;\n"
"    height: 18px;\n"
"    margin: -4px 0px -4px 0px;\n"
"    border-radius: 8px;\n"
"    background: white;\n"
"}\n"
"")
        self.widget_adjust.setObjectName("widget_adjust")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.widget_adjust)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.scrollArea = QtWidgets.QScrollArea(self.widget_adjust)
        self.scrollArea.setStyleSheet("QScrollArea{\n"
"    background-color: transparent;\n"
"}")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 301, 870))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.widget_light = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_light.setMinimumSize(QtCore.QSize(0, 88))
        self.widget_light.setMaximumSize(QtCore.QSize(16777215, 88))
        self.widget_light.setObjectName("widget_light")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_light)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_light = QtWidgets.QHBoxLayout()
        self.horizontalLayout_light.setObjectName("horizontalLayout_light")
        self.label_image_light = QtWidgets.QLabel(self.widget_light)
        self.label_image_light.setMinimumSize(QtCore.QSize(30, 30))
        self.label_image_light.setStyleSheet("image:url(:/images/icon/bright_light_control_shine_icon.svg)")
        self.label_image_light.setText("")
        self.label_image_light.setObjectName("label_image_light")
        self.horizontalLayout_light.addWidget(self.label_image_light)
        self.label_text_light = QtWidgets.QLabel(self.widget_light)
        self.label_text_light.setMinimumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_text_light.setFont(font)
        self.label_text_light.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_text_light.setObjectName("label_text_light")
        self.horizontalLayout_light.addWidget(self.label_text_light)
        self.label_light_perception = QtWidgets.QLabel(self.widget_light)
        self.label_light_perception.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_light_perception.setFont(font)
        self.label_light_perception.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_light_perception.setObjectName("label_light_perception")
        self.horizontalLayout_light.addWidget(self.label_light_perception)
        self.horizontalLayout_light.setStretch(0, 1)
        self.horizontalLayout_light.setStretch(1, 4)
        self.horizontalLayout_light.setStretch(2, 1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_light)
        self.horizontalSlider_light_perception = QtWidgets.QSlider(self.widget_light)
        self.horizontalSlider_light_perception.setStyleSheet("")
        self.horizontalSlider_light_perception.setMinimum(-100)
        self.horizontalSlider_light_perception.setMaximum(100)
        self.horizontalSlider_light_perception.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_light_perception.setObjectName("horizontalSlider_light_perception")
        self.verticalLayout_4.addWidget(self.horizontalSlider_light_perception)
        self.verticalLayout_15.addWidget(self.widget_light)
        self.widget_brightness = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_brightness.setMinimumSize(QtCore.QSize(0, 88))
        self.widget_brightness.setMaximumSize(QtCore.QSize(16777215, 88))
        self.widget_brightness.setObjectName("widget_brightness")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_brightness)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_brightness = QtWidgets.QHBoxLayout()
        self.horizontalLayout_brightness.setObjectName("horizontalLayout_brightness")
        self.label_image_brightness = QtWidgets.QLabel(self.widget_brightness)
        self.label_image_brightness.setMinimumSize(QtCore.QSize(30, 30))
        self.label_image_brightness.setStyleSheet("image:url(:/images/icon/brightness_light_icon.svg)")
        self.label_image_brightness.setText("")
        self.label_image_brightness.setObjectName("label_image_brightness")
        self.horizontalLayout_brightness.addWidget(self.label_image_brightness)
        self.label_text_brightness = QtWidgets.QLabel(self.widget_brightness)
        self.label_text_brightness.setMinimumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_text_brightness.setFont(font)
        self.label_text_brightness.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_text_brightness.setObjectName("label_text_brightness")
        self.horizontalLayout_brightness.addWidget(self.label_text_brightness)
        self.label_brightness = QtWidgets.QLabel(self.widget_brightness)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_brightness.setFont(font)
        self.label_brightness.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_brightness.setObjectName("label_brightness")
        self.horizontalLayout_brightness.addWidget(self.label_brightness)
        self.horizontalLayout_brightness.setStretch(0, 1)
        self.horizontalLayout_brightness.setStretch(1, 4)
        self.horizontalLayout_brightness.setStretch(2, 1)
        self.verticalLayout_5.addLayout(self.horizontalLayout_brightness)
        self.horizontalSlider_brightness = QtWidgets.QSlider(self.widget_brightness)
        self.horizontalSlider_brightness.setStyleSheet("")
        self.horizontalSlider_brightness.setMinimum(-100)
        self.horizontalSlider_brightness.setMaximum(100)
        self.horizontalSlider_brightness.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_brightness.setObjectName("horizontalSlider_brightness")
        self.verticalLayout_5.addWidget(self.horizontalSlider_brightness)
        self.verticalLayout_15.addWidget(self.widget_brightness)
        self.widget_exposure = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_exposure.setMinimumSize(QtCore.QSize(0, 88))
        self.widget_exposure.setMaximumSize(QtCore.QSize(16777215, 88))
        self.widget_exposure.setObjectName("widget_exposure")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.widget_exposure)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.horizontalLayout_exposure = QtWidgets.QHBoxLayout()
        self.horizontalLayout_exposure.setObjectName("horizontalLayout_exposure")
        self.label_image_exposure = QtWidgets.QLabel(self.widget_exposure)
        self.label_image_exposure.setMinimumSize(QtCore.QSize(30, 30))
        self.label_image_exposure.setStyleSheet("image:url(:/images/icon/exposure_icon.svg)")
        self.label_image_exposure.setText("")
        self.label_image_exposure.setObjectName("label_image_exposure")
        self.horizontalLayout_exposure.addWidget(self.label_image_exposure)
        self.label_text_exposure = QtWidgets.QLabel(self.widget_exposure)
        self.label_text_exposure.setMinimumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_text_exposure.setFont(font)
        self.label_text_exposure.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_text_exposure.setObjectName("label_text_exposure")
        self.horizontalLayout_exposure.addWidget(self.label_text_exposure)
        self.label_exposure = QtWidgets.QLabel(self.widget_exposure)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_exposure.setFont(font)
        self.label_exposure.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_exposure.setObjectName("label_exposure")
        self.horizontalLayout_exposure.addWidget(self.label_exposure)
        self.horizontalLayout_exposure.setStretch(0, 1)
        self.horizontalLayout_exposure.setStretch(1, 4)
        self.horizontalLayout_exposure.setStretch(2, 1)
        self.verticalLayout_14.addLayout(self.horizontalLayout_exposure)
        self.horizontalSlider_exposure = QtWidgets.QSlider(self.widget_exposure)
        self.horizontalSlider_exposure.setStyleSheet("")
        self.horizontalSlider_exposure.setMinimum(-100)
        self.horizontalSlider_exposure.setMaximum(100)
        self.horizontalSlider_exposure.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_exposure.setObjectName("horizontalSlider_exposure")
        self.verticalLayout_14.addWidget(self.horizontalSlider_exposure)
        self.verticalLayout_15.addWidget(self.widget_exposure)
        self.widget_contrast = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_contrast.setMinimumSize(QtCore.QSize(0, 88))
        self.widget_contrast.setMaximumSize(QtCore.QSize(16777215, 88))
        self.widget_contrast.setObjectName("widget_contrast")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.widget_contrast)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.horizontalLayout_contrast = QtWidgets.QHBoxLayout()
        self.horizontalLayout_contrast.setObjectName("horizontalLayout_contrast")
        self.label_image_contrast = QtWidgets.QLabel(self.widget_contrast)
        self.label_image_contrast.setMinimumSize(QtCore.QSize(30, 30))
        self.label_image_contrast.setStyleSheet("image:url(:/images/icon/contrast_brightness_setting_icon.svg)")
        self.label_image_contrast.setText("")
        self.label_image_contrast.setObjectName("label_image_contrast")
        self.horizontalLayout_contrast.addWidget(self.label_image_contrast)
        self.label_text_contrast = QtWidgets.QLabel(self.widget_contrast)
        self.label_text_contrast.setMinimumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_text_contrast.setFont(font)
        self.label_text_contrast.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_text_contrast.setObjectName("label_text_contrast")
        self.horizontalLayout_contrast.addWidget(self.label_text_contrast)
        self.label_contrast = QtWidgets.QLabel(self.widget_contrast)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_contrast.setFont(font)
        self.label_contrast.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_contrast.setObjectName("label_contrast")
        self.horizontalLayout_contrast.addWidget(self.label_contrast)
        self.horizontalLayout_contrast.setStretch(0, 1)
        self.horizontalLayout_contrast.setStretch(1, 4)
        self.horizontalLayout_contrast.setStretch(2, 1)
        self.verticalLayout_13.addLayout(self.horizontalLayout_contrast)
        self.horizontalSlider_contrast = QtWidgets.QSlider(self.widget_contrast)
        self.horizontalSlider_contrast.setStyleSheet("")
        self.horizontalSlider_contrast.setMinimum(-100)
        self.horizontalSlider_contrast.setMaximum(100)
        self.horizontalSlider_contrast.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_contrast.setObjectName("horizontalSlider_contrast")
        self.verticalLayout_13.addWidget(self.horizontalSlider_contrast)
        self.verticalLayout_15.addWidget(self.widget_contrast)
        self.widget_saturation = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_saturation.setMinimumSize(QtCore.QSize(0, 88))
        self.widget_saturation.setMaximumSize(QtCore.QSize(16777215, 88))
        self.widget_saturation.setObjectName("widget_saturation")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.widget_saturation)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_saturation = QtWidgets.QHBoxLayout()
        self.horizontalLayout_saturation.setObjectName("horizontalLayout_saturation")
        self.label_image_saturation = QtWidgets.QLabel(self.widget_saturation)
        self.label_image_saturation.setMinimumSize(QtCore.QSize(30, 30))
        self.label_image_saturation.setStyleSheet("image:url(:/images/icon/bx_tone_icon.svg)")
        self.label_image_saturation.setText("")
        self.label_image_saturation.setObjectName("label_image_saturation")
        self.horizontalLayout_saturation.addWidget(self.label_image_saturation)
        self.label_text_saturation = QtWidgets.QLabel(self.widget_saturation)
        self.label_text_saturation.setMinimumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_text_saturation.setFont(font)
        self.label_text_saturation.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_text_saturation.setObjectName("label_text_saturation")
        self.horizontalLayout_saturation.addWidget(self.label_text_saturation)
        self.label_saturation = QtWidgets.QLabel(self.widget_saturation)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_saturation.setFont(font)
        self.label_saturation.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_saturation.setObjectName("label_saturation")
        self.horizontalLayout_saturation.addWidget(self.label_saturation)
        self.horizontalLayout_saturation.setStretch(0, 1)
        self.horizontalLayout_saturation.setStretch(1, 4)
        self.horizontalLayout_saturation.setStretch(2, 1)
        self.verticalLayout_12.addLayout(self.horizontalLayout_saturation)
        self.horizontalSlider_saturation = QtWidgets.QSlider(self.widget_saturation)
        self.horizontalSlider_saturation.setStyleSheet("")
        self.horizontalSlider_saturation.setMinimum(-100)
        self.horizontalSlider_saturation.setMaximum(100)
        self.horizontalSlider_saturation.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_saturation.setObjectName("horizontalSlider_saturation")
        self.verticalLayout_12.addWidget(self.horizontalSlider_saturation)
        self.verticalLayout_15.addWidget(self.widget_saturation)
        self.widget_sharp = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_sharp.setMinimumSize(QtCore.QSize(0, 88))
        self.widget_sharp.setMaximumSize(QtCore.QSize(16777215, 88))
        self.widget_sharp.setObjectName("widget_sharp")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.widget_sharp)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_sharp = QtWidgets.QHBoxLayout()
        self.horizontalLayout_sharp.setObjectName("horizontalLayout_sharp")
        self.label_image_sharp = QtWidgets.QLabel(self.widget_sharp)
        self.label_image_sharp.setMinimumSize(QtCore.QSize(30, 30))
        self.label_image_sharp.setStyleSheet("image:url(:/images/icon/triangle_outline_icon.svg)")
        self.label_image_sharp.setText("")
        self.label_image_sharp.setObjectName("label_image_sharp")
        self.horizontalLayout_sharp.addWidget(self.label_image_sharp)
        self.label_text_sharp = QtWidgets.QLabel(self.widget_sharp)
        self.label_text_sharp.setMinimumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_text_sharp.setFont(font)
        self.label_text_sharp.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_text_sharp.setObjectName("label_text_sharp")
        self.horizontalLayout_sharp.addWidget(self.label_text_sharp)
        self.label_sharp = QtWidgets.QLabel(self.widget_sharp)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_sharp.setFont(font)
        self.label_sharp.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_sharp.setObjectName("label_sharp")
        self.horizontalLayout_sharp.addWidget(self.label_sharp)
        self.horizontalLayout_sharp.setStretch(0, 1)
        self.horizontalLayout_sharp.setStretch(1, 4)
        self.horizontalLayout_sharp.setStretch(2, 1)
        self.verticalLayout_11.addLayout(self.horizontalLayout_sharp)
        self.horizontalSlider_sharp = QtWidgets.QSlider(self.widget_sharp)
        self.horizontalSlider_sharp.setStyleSheet("")
        self.horizontalSlider_sharp.setMinimum(-100)
        self.horizontalSlider_sharp.setMaximum(100)
        self.horizontalSlider_sharp.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_sharp.setObjectName("horizontalSlider_sharp")
        self.verticalLayout_11.addWidget(self.horizontalSlider_sharp)
        self.verticalLayout_15.addWidget(self.widget_sharp)
        self.widget_smooth = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_smooth.setMinimumSize(QtCore.QSize(0, 88))
        self.widget_smooth.setMaximumSize(QtCore.QSize(16777215, 88))
        self.widget_smooth.setObjectName("widget_smooth")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.widget_smooth)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_smooth = QtWidgets.QHBoxLayout()
        self.horizontalLayout_smooth.setObjectName("horizontalLayout_smooth")
        self.label_image_smooth = QtWidgets.QLabel(self.widget_smooth)
        self.label_image_smooth.setMinimumSize(QtCore.QSize(30, 30))
        self.label_image_smooth.setStyleSheet("image:url(:/images/icon/curve_auto_colon_icon.svg)")
        self.label_image_smooth.setText("")
        self.label_image_smooth.setObjectName("label_image_smooth")
        self.horizontalLayout_smooth.addWidget(self.label_image_smooth)
        self.label_text_smooth = QtWidgets.QLabel(self.widget_smooth)
        self.label_text_smooth.setMinimumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_text_smooth.setFont(font)
        self.label_text_smooth.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_text_smooth.setObjectName("label_text_smooth")
        self.horizontalLayout_smooth.addWidget(self.label_text_smooth)
        self.label_smooth = QtWidgets.QLabel(self.widget_smooth)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_smooth.setFont(font)
        self.label_smooth.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_smooth.setObjectName("label_smooth")
        self.horizontalLayout_smooth.addWidget(self.label_smooth)
        self.horizontalLayout_smooth.setStretch(0, 1)
        self.horizontalLayout_smooth.setStretch(1, 4)
        self.horizontalLayout_smooth.setStretch(2, 1)
        self.verticalLayout_10.addLayout(self.horizontalLayout_smooth)
        self.horizontalSlider_smooth = QtWidgets.QSlider(self.widget_smooth)
        self.horizontalSlider_smooth.setStyleSheet("")
        self.horizontalSlider_smooth.setMinimum(-100)
        self.horizontalSlider_smooth.setMaximum(100)
        self.horizontalSlider_smooth.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_smooth.setObjectName("horizontalSlider_smooth")
        self.verticalLayout_10.addWidget(self.horizontalSlider_smooth)
        self.verticalLayout_15.addWidget(self.widget_smooth)
        self.widget_temperature = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_temperature.setMinimumSize(QtCore.QSize(0, 88))
        self.widget_temperature.setMaximumSize(QtCore.QSize(16777215, 88))
        self.widget_temperature.setObjectName("widget_temperature")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_temperature)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_temperature = QtWidgets.QHBoxLayout()
        self.horizontalLayout_temperature.setObjectName("horizontalLayout_temperature")
        self.label_image_temperature = QtWidgets.QLabel(self.widget_temperature)
        self.label_image_temperature.setMinimumSize(QtCore.QSize(30, 30))
        self.label_image_temperature.setStyleSheet("image:url(:/images/icon/thermometer_high_icon.svg)")
        self.label_image_temperature.setText("")
        self.label_image_temperature.setObjectName("label_image_temperature")
        self.horizontalLayout_temperature.addWidget(self.label_image_temperature)
        self.label_text_temperature = QtWidgets.QLabel(self.widget_temperature)
        self.label_text_temperature.setMinimumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_text_temperature.setFont(font)
        self.label_text_temperature.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_text_temperature.setObjectName("label_text_temperature")
        self.horizontalLayout_temperature.addWidget(self.label_text_temperature)
        self.label_temperature = QtWidgets.QLabel(self.widget_temperature)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_temperature.setFont(font)
        self.label_temperature.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_temperature.setObjectName("label_temperature")
        self.horizontalLayout_temperature.addWidget(self.label_temperature)
        self.horizontalLayout_temperature.setStretch(0, 1)
        self.horizontalLayout_temperature.setStretch(1, 4)
        self.horizontalLayout_temperature.setStretch(2, 1)
        self.verticalLayout_9.addLayout(self.horizontalLayout_temperature)
        self.horizontalSlider_temperature = QtWidgets.QSlider(self.widget_temperature)
        self.horizontalSlider_temperature.setStyleSheet("")
        self.horizontalSlider_temperature.setMinimum(-100)
        self.horizontalSlider_temperature.setMaximum(100)
        self.horizontalSlider_temperature.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_temperature.setObjectName("horizontalSlider_temperature")
        self.verticalLayout_9.addWidget(self.horizontalSlider_temperature)
        self.verticalLayout_15.addWidget(self.widget_temperature)
        self.widget_tone = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_tone.setMinimumSize(QtCore.QSize(0, 88))
        self.widget_tone.setMaximumSize(QtCore.QSize(16777215, 88))
        self.widget_tone.setObjectName("widget_tone")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.widget_tone)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_tone = QtWidgets.QHBoxLayout()
        self.horizontalLayout_tone.setObjectName("horizontalLayout_tone")
        self.label_image_tone = QtWidgets.QLabel(self.widget_tone)
        self.label_image_tone.setMinimumSize(QtCore.QSize(30, 30))
        self.label_image_tone.setStyleSheet("image:url(:/images/icon/bx_color_fill_icon.svg)")
        self.label_image_tone.setText("")
        self.label_image_tone.setObjectName("label_image_tone")
        self.horizontalLayout_tone.addWidget(self.label_image_tone)
        self.label_text_tone = QtWidgets.QLabel(self.widget_tone)
        self.label_text_tone.setMinimumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_text_tone.setFont(font)
        self.label_text_tone.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_text_tone.setObjectName("label_text_tone")
        self.horizontalLayout_tone.addWidget(self.label_text_tone)
        self.label_tone = QtWidgets.QLabel(self.widget_tone)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_tone.setFont(font)
        self.label_tone.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_tone.setObjectName("label_tone")
        self.horizontalLayout_tone.addWidget(self.label_tone)
        self.horizontalLayout_tone.setStretch(0, 1)
        self.horizontalLayout_tone.setStretch(1, 4)
        self.horizontalLayout_tone.setStretch(2, 1)
        self.verticalLayout_8.addLayout(self.horizontalLayout_tone)
        self.horizontalSlider_tone = QtWidgets.QSlider(self.widget_tone)
        self.horizontalSlider_tone.setStyleSheet("")
        self.horizontalSlider_tone.setMinimum(-100)
        self.horizontalSlider_tone.setMaximum(100)
        self.horizontalSlider_tone.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_tone.setObjectName("horizontalSlider_tone")
        self.verticalLayout_8.addWidget(self.horizontalSlider_tone)
        self.verticalLayout_15.addWidget(self.widget_tone)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_18.addWidget(self.scrollArea)
        self.horizontalLayout.addWidget(self.widget_adjust)

        self.retranslateUi(Form)
        self.horizontalSlider_brightness.valueChanged['int'].connect(self.label_brightness.setNum) # type: ignore
        self.horizontalSlider_contrast.valueChanged['int'].connect(self.label_contrast.setNum) # type: ignore
        self.horizontalSlider_exposure.valueChanged['int'].connect(self.label_exposure.setNum) # type: ignore
        self.horizontalSlider_light_perception.valueChanged['int'].connect(self.label_light_perception.setNum) # type: ignore
        self.horizontalSlider_saturation.valueChanged['int'].connect(self.label_saturation.setNum) # type: ignore
        self.horizontalSlider_sharp.valueChanged['int'].connect(self.label_sharp.setNum) # type: ignore
        self.horizontalSlider_smooth.valueChanged['int'].connect(self.label_smooth.setNum) # type: ignore
        self.horizontalSlider_temperature.valueChanged['int'].connect(self.label_temperature.setNum) # type: ignore
        self.horizontalSlider_tone.valueChanged['int'].connect(self.label_tone.setNum) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_text_light.setText(_translate("Form", "光感"))
        self.label_light_perception.setText(_translate("Form", "0"))
        self.label_text_brightness.setText(_translate("Form", "亮度"))
        self.label_brightness.setText(_translate("Form", "0"))
        self.label_text_exposure.setText(_translate("Form", "曝光"))
        self.label_exposure.setText(_translate("Form", "0"))
        self.label_text_contrast.setText(_translate("Form", "对比度"))
        self.label_contrast.setText(_translate("Form", "0"))
        self.label_text_saturation.setText(_translate("Form", "饱和度"))
        self.label_saturation.setText(_translate("Form", "0"))
        self.label_text_sharp.setText(_translate("Form", "锐化"))
        self.label_sharp.setText(_translate("Form", "0"))
        self.label_text_smooth.setText(_translate("Form", "平滑"))
        self.label_smooth.setText(_translate("Form", "0"))
        self.label_text_temperature.setText(_translate("Form", "色温"))
        self.label_temperature.setText(_translate("Form", "0"))
        self.label_text_tone.setText(_translate("Form", "色调"))
        self.label_tone.setText(_translate("Form", "0"))
import resources_rc