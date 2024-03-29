# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_xml/widget_function_stack.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(664, 86)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.function_stack = QtWidgets.QStackedWidget(Form)
        self.function_stack.setStyleSheet("QStackedWidget{\n"
"                            background-color:transparent;\n"
"                            }\n"
"                        ")
        self.function_stack.setObjectName("function_stack")
        self.page_crop = QtWidgets.QWidget()
        self.page_crop.setObjectName("page_crop")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.page_crop)
        self.horizontalLayout_13.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        spacerItem = QtWidgets.QSpacerItem(404, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem)
        self.widget_crop = QtWidgets.QWidget(self.page_crop)
        self.widget_crop.setMinimumSize(QtCore.QSize(150, 0))
        self.widget_crop.setStyleSheet("QWidget{\n"
"                                            background-color: rgb(32, 32, 32);\n"
"                                            border-radius:25px;\n"
"                                            }\n"
"                                        ")
        self.widget_crop.setObjectName("widget_crop")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.widget_crop)
        self.horizontalLayout_15.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.pushButton_apply = QtWidgets.QPushButton(self.widget_crop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_apply.sizePolicy().hasHeightForWidth())
        self.pushButton_apply.setSizePolicy(sizePolicy)
        self.pushButton_apply.setMinimumSize(QtCore.QSize(48, 44))
        self.pushButton_apply.setMaximumSize(QtCore.QSize(48, 44))
        self.pushButton_apply.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_apply.setToolTipDuration(3000)
        self.pushButton_apply.setStyleSheet(".QPushButton:hover{\n"
"                                                        background-color:rgb(58, 58, 58);\n"
"                                                        border-radius:10px;\n"
"                                                        }\n"
"                                                    ")
        self.pushButton_apply.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icon/apply_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_apply.setIcon(icon)
        self.pushButton_apply.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_apply.setFlat(True)
        self.pushButton_apply.setObjectName("pushButton_apply")
        self.horizontalLayout_15.addWidget(self.pushButton_apply)
        self.pushButton_cancel = QtWidgets.QPushButton(self.widget_crop)
        self.pushButton_cancel.setMinimumSize(QtCore.QSize(48, 44))
        self.pushButton_cancel.setMaximumSize(QtCore.QSize(48, 44))
        self.pushButton_cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_cancel.setToolTipDuration(3000)
        self.pushButton_cancel.setStyleSheet(".QPushButton:hover{\n"
"                                                        background-color:rgb(58, 58, 58);\n"
"                                                        border-radius:10px;\n"
"                                                        }\n"
"                                                    ")
        self.pushButton_cancel.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/icon/cancel_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_cancel.setIcon(icon1)
        self.pushButton_cancel.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_cancel.setFlat(True)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout_15.addWidget(self.pushButton_cancel)
        self.separator_crop = QtWidgets.QWidget(self.widget_crop)
        self.separator_crop.setMinimumSize(QtCore.QSize(41, 0))
        self.separator_crop.setStyleSheet("image:url(:/images/icon/vertical_line_icon.svg);\n"
"                                                        background-color: transparent;\n"
"                                                    ")
        self.separator_crop.setObjectName("separator_crop")
        self.horizontalLayout_15.addWidget(self.separator_crop)
        self.slider_rotate = QtWidgets.QSlider(self.widget_crop)
        self.slider_rotate.setMinimumSize(QtCore.QSize(140, 0))
        self.slider_rotate.setStyleSheet("\n"
"QSlider::groove:horizontal {\n"
"background:  qlineargradient(spread: pad, x1: 0, y1: 1, x2: 1, y2: 1,\n"
"stop: 0 rgb(51, 151, 255),\n"
"stop: 0.5 rgb(100, 100, 100),\n"
"stop: 1 rgb(255, 78, 0,));\n"
"height: 8px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"width: 16px;\n"
"height: 18px;\n"
"margin: -4px 0px -4px 0px;\n"
"border-radius: 8px;\n"
"background: white;\n"
"}\n"
"                                                    ")
        self.slider_rotate.setMinimum(-45)
        self.slider_rotate.setMaximum(45)
        self.slider_rotate.setOrientation(QtCore.Qt.Horizontal)
        self.slider_rotate.setObjectName("slider_rotate")
        self.horizontalLayout_15.addWidget(self.slider_rotate)
        self.label_rotate = QtWidgets.QLabel(self.widget_crop)
        self.label_rotate.setMinimumSize(QtCore.QSize(30, 44))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        self.label_rotate.setFont(font)
        self.label_rotate.setStyleSheet("QLabel{\n"
"                                                        color: rgb(255, 255, 255);\n"
"                                                        background-color: transparent;\n"
"                                                        }\n"
"                                                    ")
        self.label_rotate.setObjectName("label_rotate")
        self.horizontalLayout_15.addWidget(self.label_rotate)
        self.horizontalLayout_13.addWidget(self.widget_crop)
        spacerItem1 = QtWidgets.QSpacerItem(404, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem1)
        self.horizontalLayout_13.setStretch(0, 1)
        self.horizontalLayout_13.setStretch(2, 1)
        self.function_stack.addWidget(self.page_crop)
        self.page_rotate = QtWidgets.QWidget()
        self.page_rotate.setObjectName("page_rotate")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.page_rotate)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem2)
        self.widget_rotate = QtWidgets.QWidget(self.page_rotate)
        self.widget_rotate.setMinimumSize(QtCore.QSize(150, 0))
        self.widget_rotate.setStyleSheet("QWidget{\n"
"                                            background-color: rgb(32, 32, 32);\n"
"                                            border-radius:25px;\n"
"                                            }\n"
"                                        ")
        self.widget_rotate.setObjectName("widget_rotate")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.widget_rotate)
        self.horizontalLayout_14.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.pushButton_left_90 = QtWidgets.QPushButton(self.widget_rotate)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_left_90.sizePolicy().hasHeightForWidth())
        self.pushButton_left_90.setSizePolicy(sizePolicy)
        self.pushButton_left_90.setMinimumSize(QtCore.QSize(48, 44))
        self.pushButton_left_90.setMaximumSize(QtCore.QSize(48, 44))
        self.pushButton_left_90.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_left_90.setToolTipDuration(3000)
        self.pushButton_left_90.setStyleSheet(".QPushButton:hover{\n"
"                                                        background-color:rgb(58, 58, 58);\n"
"                                                        border-radius:10px;\n"
"                                                        }\n"
"                                                    ")
        self.pushButton_left_90.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/icon/rotate_counterclockwise_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_left_90.setIcon(icon2)
        self.pushButton_left_90.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_left_90.setFlat(True)
        self.pushButton_left_90.setObjectName("pushButton_left_90")
        self.horizontalLayout_14.addWidget(self.pushButton_left_90)
        self.pushButton_right_90 = QtWidgets.QPushButton(self.widget_rotate)
        self.pushButton_right_90.setMinimumSize(QtCore.QSize(48, 44))
        self.pushButton_right_90.setMaximumSize(QtCore.QSize(48, 44))
        self.pushButton_right_90.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_right_90.setToolTipDuration(3000)
        self.pushButton_right_90.setStyleSheet(".QPushButton:hover{\n"
"                                                        background-color:rgb(58, 58, 58);\n"
"                                                        border-radius:10px;\n"
"                                                        }\n"
"                                                    ")
        self.pushButton_right_90.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/icon/rotate_clockwise_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_right_90.setIcon(icon3)
        self.pushButton_right_90.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_right_90.setFlat(True)
        self.pushButton_right_90.setObjectName("pushButton_right_90")
        self.horizontalLayout_14.addWidget(self.pushButton_right_90)
        self.pushButton_flip_y = QtWidgets.QPushButton(self.widget_rotate)
        self.pushButton_flip_y.setMinimumSize(QtCore.QSize(48, 44))
        self.pushButton_flip_y.setMaximumSize(QtCore.QSize(48, 44))
        self.pushButton_flip_y.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_flip_y.setToolTipDuration(3000)
        self.pushButton_flip_y.setStyleSheet(".QPushButton:hover{\n"
"                                                        background-color:rgb(58, 58, 58);\n"
"                                                        border-radius:10px;\n"
"                                                        }\n"
"                                                    ")
        self.pushButton_flip_y.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/icon/ic-flip-y.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_flip_y.setIcon(icon4)
        self.pushButton_flip_y.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_flip_y.setFlat(True)
        self.pushButton_flip_y.setObjectName("pushButton_flip_y")
        self.horizontalLayout_14.addWidget(self.pushButton_flip_y)
        self.pushButton_flip_x = QtWidgets.QPushButton(self.widget_rotate)
        self.pushButton_flip_x.setMinimumSize(QtCore.QSize(48, 44))
        self.pushButton_flip_x.setMaximumSize(QtCore.QSize(48, 44))
        self.pushButton_flip_x.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_flip_x.setToolTipDuration(3000)
        self.pushButton_flip_x.setStyleSheet(".QPushButton:hover{\n"
"                                                        background-color:rgb(58, 58, 58);\n"
"                                                        border-radius:10px;\n"
"                                                        }\n"
"                                                    ")
        self.pushButton_flip_x.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/icon/ic-flip-x.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_flip_x.setIcon(icon5)
        self.pushButton_flip_x.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_flip_x.setFlat(True)
        self.pushButton_flip_x.setObjectName("pushButton_flip_x")
        self.horizontalLayout_14.addWidget(self.pushButton_flip_x)
        self.horizontalLayout_16.addWidget(self.widget_rotate)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem3)
        self.function_stack.addWidget(self.page_rotate)
        self.page_text = QtWidgets.QWidget()
        self.page_text.setObjectName("page_text")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.page_text)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(116, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.widget_text = QtWidgets.QWidget(self.page_text)
        self.widget_text.setMinimumSize(QtCore.QSize(150, 0))
        self.widget_text.setStyleSheet("QWidget{\n"
"                                            background-color: rgb(32, 32, 32);\n"
"                                            border-radius:25px;\n"
"                                            }\n"
"                                        ")
        self.widget_text.setObjectName("widget_text")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.widget_text)
        self.horizontalLayout_18.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.spinBox = QtWidgets.QSpinBox(self.widget_text)
        self.spinBox.setMinimumSize(QtCore.QSize(94, 44))
        self.spinBox.setMaximumSize(QtCore.QSize(94, 44))
        self.spinBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.spinBox.setStyleSheet("QSpinBox {\n"
"                                                        font-size: 18px;\n"
"                                                        font-weight: bold;\n"
"                                                        padding:0px;\n"
"                                                        font-family: \"黑体\";\n"
"                                                        color:rgb(255, 255, 255);\n"
"                                                        }\n"
"                                                        QSpinBox::up-button {\n"
"                                                        subcontrol-position: right;\n"
"                                                        image: url(:/images/icon/font_increase_icon.svg);\n"
"                                                        }\n"
"                                                        QSpinBox::down-button {\n"
"                                                        subcontrol-position: left;\n"
"                                                        margin:0px;\n"
"                                                        image: url(:/images/icon/font_decrease_icon.svg);\n"
"                                                        }\n"
"                                                        QSpinBox::up-button:hover, QSpinBox::down-button:hover {\n"
"                                                        background-color:rgb(58, 58, 58);\n"
"                                                        margin:0px;\n"
"                                                        border-radius:10px;\n"
"                                                        }\n"
"                                                    ")
        self.spinBox.setAccelerated(True)
        self.spinBox.setMinimum(10)
        self.spinBox.setMaximum(96)
        self.spinBox.setProperty("value", 24)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_18.addWidget(self.spinBox)
        self.pushButton_text_color = QtWidgets.QPushButton(self.widget_text)
        self.pushButton_text_color.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_text_color.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_text_color.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_text_color.setStyleSheet(".QPushButton{\n"
"                                                        background-color:#FFFFFF;\n"
"                                                        border-radius:15px;\n"
"                                                        }\n"
"                                                    ")
        self.pushButton_text_color.setFlat(True)
        self.pushButton_text_color.setObjectName("pushButton_text_color")
        self.horizontalLayout_18.addWidget(self.pushButton_text_color)
        self.pushButton_font = QtWidgets.QPushButton(self.widget_text)
        self.pushButton_font.setMinimumSize(QtCore.QSize(48, 44))
        self.pushButton_font.setMaximumSize(QtCore.QSize(48, 44))
        self.pushButton_font.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_font.setToolTipDuration(3000)
        self.pushButton_font.setStyleSheet(".QPushButton:hover{\n"
"                                                        background-color:rgb(58, 58, 58);\n"
"                                                        border-radius:10px;\n"
"                                                        }\n"
"                                                    ")
        self.pushButton_font.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/icon/font_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_font.setIcon(icon6)
        self.pushButton_font.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_font.setFlat(True)
        self.pushButton_font.setObjectName("pushButton_font")
        self.horizontalLayout_18.addWidget(self.pushButton_font)
        self.separator_text = QtWidgets.QWidget(self.widget_text)
        self.separator_text.setMinimumSize(QtCore.QSize(41, 0))
        self.separator_text.setStyleSheet("image:url(:/images/icon/vertical_line_icon.svg);\n"
"                                                        background-color: transparent;\n"
"                                                    ")
        self.separator_text.setObjectName("separator_text")
        self.horizontalLayout_18.addWidget(self.separator_text)
        self.pushButton_apply_text = QtWidgets.QPushButton(self.widget_text)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_apply_text.sizePolicy().hasHeightForWidth())
        self.pushButton_apply_text.setSizePolicy(sizePolicy)
        self.pushButton_apply_text.setMinimumSize(QtCore.QSize(48, 44))
        self.pushButton_apply_text.setMaximumSize(QtCore.QSize(48, 44))
        self.pushButton_apply_text.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_apply_text.setToolTipDuration(3000)
        self.pushButton_apply_text.setStyleSheet(".QPushButton:hover{\n"
"                                                        background-color:rgb(58, 58, 58);\n"
"                                                        border-radius:10px;\n"
"                                                        }\n"
"                                                    ")
        self.pushButton_apply_text.setText("")
        self.pushButton_apply_text.setIcon(icon)
        self.pushButton_apply_text.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_apply_text.setFlat(True)
        self.pushButton_apply_text.setObjectName("pushButton_apply_text")
        self.horizontalLayout_18.addWidget(self.pushButton_apply_text)
        self.pushButton_cancel_text = QtWidgets.QPushButton(self.widget_text)
        self.pushButton_cancel_text.setMinimumSize(QtCore.QSize(48, 44))
        self.pushButton_cancel_text.setMaximumSize(QtCore.QSize(48, 44))
        self.pushButton_cancel_text.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_cancel_text.setToolTipDuration(3000)
        self.pushButton_cancel_text.setStyleSheet(".QPushButton:hover{\n"
"                                                        background-color:rgb(58, 58, 58);\n"
"                                                        border-radius:10px;\n"
"                                                        }\n"
"                                                    ")
        self.pushButton_cancel_text.setText("")
        self.pushButton_cancel_text.setIcon(icon1)
        self.pushButton_cancel_text.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_cancel_text.setFlat(True)
        self.pushButton_cancel_text.setObjectName("pushButton_cancel_text")
        self.horizontalLayout_18.addWidget(self.pushButton_cancel_text)
        self.horizontalLayout_2.addWidget(self.widget_text)
        spacerItem5 = QtWidgets.QSpacerItem(115, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.function_stack.addWidget(self.page_text)
        self.horizontalLayout.addWidget(self.function_stack)

        self.retranslateUi(Form)
        self.function_stack.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_apply.setToolTip(_translate("Form", "应用"))
        self.pushButton_cancel.setToolTip(_translate("Form", "取消"))
        self.label_rotate.setText(_translate("Form", "0°"))
        self.pushButton_left_90.setToolTip(_translate("Form", "逆时针旋转90°"))
        self.pushButton_right_90.setToolTip(_translate("Form", "顺时针旋转90°"))
        self.pushButton_flip_y.setToolTip(_translate("Form", "上下翻转"))
        self.pushButton_flip_x.setToolTip(_translate("Form", "左右翻转"))
        self.pushButton_font.setToolTip(_translate("Form", "字体"))
        self.pushButton_apply_text.setToolTip(_translate("Form", "应用"))
        self.pushButton_cancel_text.setToolTip(_translate("Form", "取消"))
import resources_rc
