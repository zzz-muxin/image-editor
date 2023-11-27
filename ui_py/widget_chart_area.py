# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_xml/widget_chart_area.ui'
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
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_hist = QtWidgets.QWidget(Form)
        self.widget_hist.setStyleSheet("QWidget{\n"
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
        self.widget_hist.setObjectName("widget_hist")
        self.horizontalLayout_hist = QtWidgets.QHBoxLayout(self.widget_hist)
        self.horizontalLayout_hist.setObjectName("horizontalLayout_hist")
        self.scrollArea = QtWidgets.QScrollArea(self.widget_hist)
        self.scrollArea.setStyleSheet("QScrollArea{\n"
"    background-color: transparent;\n"
"}")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 301, 892))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_color_button = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_color_button.setStyleSheet(".QPushButton:hover{\n"
"    background-color:rgb(100, 100, 100);\n"
"    border-radius:20px;\n"
"}\n"
".QPushButton:pressed{\n"
"    background-color:rgb(50, 50, 50);\n"
"    border-radius:20px;\n"
"}\n"
".QPushButton:normal{\n"
"    background-color:transparent;\n"
"    border-radius:20px;\n"
"}\n"
".QPushButton:checked{\n"
"    background-color:rgb(255, 255, 255);\n"
"    border-radius:20px;\n"
"}")
        self.widget_color_button.setObjectName("widget_color_button")
        self.horizontalLayout_color_button = QtWidgets.QHBoxLayout(self.widget_color_button)
        self.horizontalLayout_color_button.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_color_button.setObjectName("horizontalLayout_color_button")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_color_button.addItem(spacerItem)
        self.pushButton_colorful = QtWidgets.QPushButton(self.widget_color_button)
        self.pushButton_colorful.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton_colorful.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_colorful.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icon/colorful.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_colorful.setIcon(icon)
        self.pushButton_colorful.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_colorful.setCheckable(True)
        self.pushButton_colorful.setAutoExclusive(True)
        self.pushButton_colorful.setFlat(True)
        self.pushButton_colorful.setObjectName("pushButton_colorful")
        self.horizontalLayout_color_button.addWidget(self.pushButton_colorful)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_color_button.addItem(spacerItem1)
        self.pushButton_red = QtWidgets.QPushButton(self.widget_color_button)
        self.pushButton_red.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton_red.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_red.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/icon/red_circle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_red.setIcon(icon1)
        self.pushButton_red.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_red.setCheckable(True)
        self.pushButton_red.setAutoExclusive(True)
        self.pushButton_red.setFlat(True)
        self.pushButton_red.setObjectName("pushButton_red")
        self.horizontalLayout_color_button.addWidget(self.pushButton_red)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_color_button.addItem(spacerItem2)
        self.pushButton_green = QtWidgets.QPushButton(self.widget_color_button)
        self.pushButton_green.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton_green.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_green.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/icon/green_circle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_green.setIcon(icon2)
        self.pushButton_green.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_green.setCheckable(True)
        self.pushButton_green.setAutoExclusive(True)
        self.pushButton_green.setFlat(True)
        self.pushButton_green.setObjectName("pushButton_green")
        self.horizontalLayout_color_button.addWidget(self.pushButton_green)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_color_button.addItem(spacerItem3)
        self.pushButton_blue = QtWidgets.QPushButton(self.widget_color_button)
        self.pushButton_blue.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton_blue.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_blue.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/icon/blue_circle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_blue.setIcon(icon3)
        self.pushButton_blue.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_blue.setCheckable(True)
        self.pushButton_blue.setAutoExclusive(True)
        self.pushButton_blue.setFlat(True)
        self.pushButton_blue.setObjectName("pushButton_blue")
        self.horizontalLayout_color_button.addWidget(self.pushButton_blue)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_color_button.addItem(spacerItem4)
        self.verticalLayout_2.addWidget(self.widget_color_button)
        self.widget_curve = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_curve.setMinimumSize(QtCore.QSize(0, 250))
        self.widget_curve.setObjectName("widget_curve")
        self.verticalLayout_curve = QtWidgets.QVBoxLayout(self.widget_curve)
        self.verticalLayout_curve.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_curve.setObjectName("verticalLayout_curve")
        self.verticalLayout_2.addWidget(self.widget_curve)
        self.widget_equalize = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_equalize.setObjectName("widget_equalize")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_equalize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.label_hist = QtWidgets.QLabel(self.widget_equalize)
        self.label_hist.setMinimumSize(QtCore.QSize(140, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_hist.setFont(font)
        self.label_hist.setStyleSheet("QLabel{\n"
"    color:rgb(255, 255, 255);\n"
"}")
        self.label_hist.setObjectName("label_hist")
        self.horizontalLayout_2.addWidget(self.label_hist)
        self.widget_switch_button = QtWidgets.QWidget(self.widget_equalize)
        self.widget_switch_button.setMinimumSize(QtCore.QSize(60, 30))
        self.widget_switch_button.setObjectName("widget_switch_button")
        self.horizontalLayout_switch = QtWidgets.QHBoxLayout(self.widget_switch_button)
        self.horizontalLayout_switch.setContentsMargins(0, 0, 3, 0)
        self.horizontalLayout_switch.setObjectName("horizontalLayout_switch")
        self.horizontalLayout_2.addWidget(self.widget_switch_button)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.verticalLayout_2.addWidget(self.widget_equalize)
        self.widget_gray_hist = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_gray_hist.setMinimumSize(QtCore.QSize(0, 250))
        self.widget_gray_hist.setObjectName("widget_gray_hist")
        self.verticalLayout_gray_hist = QtWidgets.QVBoxLayout(self.widget_gray_hist)
        self.verticalLayout_gray_hist.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_gray_hist.setObjectName("verticalLayout_gray_hist")
        self.verticalLayout_2.addWidget(self.widget_gray_hist)
        self.widget_color_hist = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget_color_hist.setMinimumSize(QtCore.QSize(0, 250))
        self.widget_color_hist.setObjectName("widget_color_hist")
        self.verticalLayout_rgb_hist = QtWidgets.QVBoxLayout(self.widget_color_hist)
        self.verticalLayout_rgb_hist.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_rgb_hist.setObjectName("verticalLayout_rgb_hist")
        self.verticalLayout_2.addWidget(self.widget_color_hist)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_hist.addWidget(self.scrollArea)
        self.horizontalLayout.addWidget(self.widget_hist)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_hist.setText(_translate("Form", "直方图均衡化"))
import resources_rc
