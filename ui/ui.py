# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'v1ftDyLC.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSlider, QSpinBox, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1150, 700)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1150, 700))
        MainWindow.setMaximumSize(QSize(1150, 700))
        MainWindow.setBaseSize(QSize(1150, 700))
        font = QFont()
        font.setBold(True)
        font.setHintingPreference(QFont.PreferDefaultHinting)
        MainWindow.setFont(font)
        MainWindow.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_video = QLabel(self.centralwidget)
        self.label_video.setObjectName(u"label_video")
        self.label_video.setGeometry(QRect(30, 30, 640, 640))
        self.label_video.setMouseTracking(False)
        self.label_video.setFrameShape(QFrame.Shape.Box)
        self.label_video.setLineWidth(5)
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(680, 480, 461, 198))
        self.gridLayout_1 = QGridLayout(self.layoutWidget)
        self.gridLayout_1.setObjectName(u"gridLayout_1")
        self.gridLayout_1.setContentsMargins(0, 0, 0, 0)
        self.btn_reset_vx = QPushButton(self.layoutWidget)
        self.btn_reset_vx.setObjectName(u"btn_reset_vx")
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setHintingPreference(QFont.PreferDefaultHinting)
        self.btn_reset_vx.setFont(font1)

        self.gridLayout_1.addWidget(self.btn_reset_vx, 0, 2, 1, 1)

        self.sli_wz = QSlider(self.layoutWidget)
        self.sli_wz.setObjectName(u"sli_wz")
        self.sli_wz.setFont(font1)
        self.sli_wz.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_1.addWidget(self.sli_wz, 1, 1, 1, 1)

        self.label_wz = QLabel(self.layoutWidget)
        self.label_wz.setObjectName(u"label_wz")
        self.label_wz.setFont(font1)

        self.gridLayout_1.addWidget(self.label_wz, 2, 0, 1, 1)

        self.btn_reset_wx = QPushButton(self.layoutWidget)
        self.btn_reset_wx.setObjectName(u"btn_reset_wx")
        self.btn_reset_wx.setFont(font1)

        self.gridLayout_1.addWidget(self.btn_reset_wx, 2, 2, 1, 1)

        self.btn_reset_wz = QPushButton(self.layoutWidget)
        self.btn_reset_wz.setObjectName(u"btn_reset_wz")
        self.btn_reset_wz.setFont(font1)

        self.gridLayout_1.addWidget(self.btn_reset_wz, 1, 2, 1, 1)

        self.sli_wx = QSlider(self.layoutWidget)
        self.sli_wx.setObjectName(u"sli_wx")
        self.sli_wx.setFont(font1)
        self.sli_wx.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_1.addWidget(self.sli_wx, 2, 1, 1, 1)

        self.label_vx = QLabel(self.layoutWidget)
        self.label_vx.setObjectName(u"label_vx")
        self.label_vx.setFont(font1)

        self.gridLayout_1.addWidget(self.label_vx, 0, 0, 1, 1)

        self.btn_reset_all = QPushButton(self.layoutWidget)
        self.btn_reset_all.setObjectName(u"btn_reset_all")
        self.btn_reset_all.setFont(font1)

        self.gridLayout_1.addWidget(self.btn_reset_all, 3, 0, 1, 3)

        self.label_wx = QLabel(self.layoutWidget)
        self.label_wx.setObjectName(u"label_wx")
        self.label_wx.setFont(font1)

        self.gridLayout_1.addWidget(self.label_wx, 1, 0, 1, 1)

        self.btn_save_plot = QPushButton(self.layoutWidget)
        self.btn_save_plot.setObjectName(u"btn_save_plot")
        self.btn_save_plot.setFont(font1)

        self.gridLayout_1.addWidget(self.btn_save_plot, 4, 0, 1, 3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_vx_bw = QPushButton(self.layoutWidget)
        self.btn_vx_bw.setObjectName(u"btn_vx_bw")
        self.btn_vx_bw.setFont(font1)

        self.horizontalLayout.addWidget(self.btn_vx_bw)

        self.rotation_vx = QSpinBox(self.layoutWidget)
        self.rotation_vx.setObjectName(u"rotation_vx")
        self.rotation_vx.setFont(font1)
        self.rotation_vx.setMinimum(1)
        self.rotation_vx.setMaximum(100)

        self.horizontalLayout.addWidget(self.rotation_vx)

        self.btn_vx_fw = QPushButton(self.layoutWidget)
        self.btn_vx_fw.setObjectName(u"btn_vx_fw")
        self.btn_vx_fw.setFont(font1)

        self.horizontalLayout.addWidget(self.btn_vx_fw)


        self.gridLayout_1.addLayout(self.horizontalLayout, 0, 1, 1, 1)

        self.layoutWidget1 = QWidget(self.centralwidget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(680, 415, 461, 57))
        font2 = QFont()
        font2.setPointSize(25)
        font2.setBold(True)
        font2.setHintingPreference(QFont.PreferDefaultHinting)
        self.layoutWidget1.setFont(font2)
        self.gridLayout_3 = QGridLayout(self.layoutWidget1)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_id = QLabel(self.layoutWidget1)
        self.label_id.setObjectName(u"label_id")
        self.label_id.setFont(font2)

        self.gridLayout_3.addWidget(self.label_id, 0, 0, 1, 1)

        self.sb_id_tracking = QSpinBox(self.layoutWidget1)
        self.sb_id_tracking.setObjectName(u"sb_id_tracking")
        self.sb_id_tracking.setFont(font2)

        self.gridLayout_3.addWidget(self.sb_id_tracking, 0, 1, 1, 1)

        self.btn_tracking = QPushButton(self.layoutWidget1)
        self.btn_tracking.setObjectName(u"btn_tracking")
        self.btn_tracking.setFont(font2)

        self.gridLayout_3.addWidget(self.btn_tracking, 0, 2, 1, 1)

        self.gridLayout_3.setColumnStretch(1, 1)
        self.gridLayout_3.setColumnStretch(2, 1)
        self.layoutWidget2 = QWidget(self.centralwidget)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(680, 350, 461, 51))
        self.layoutWidget2.setFont(font2)
        self.gridLayout_4 = QGridLayout(self.layoutWidget2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_count_detect = QLabel(self.layoutWidget2)
        self.label_count_detect.setObjectName(u"label_count_detect")
        self.label_count_detect.setFont(font2)

        self.gridLayout_4.addWidget(self.label_count_detect, 0, 1, 1, 1)

        self.label_count = QLabel(self.layoutWidget2)
        self.label_count.setObjectName(u"label_count")
        self.label_count.setFont(font2)

        self.gridLayout_4.addWidget(self.label_count, 0, 0, 1, 1)

        self.layoutWidget3 = QWidget(self.centralwidget)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(680, 30, 461, 74))
        self.gridLayout_5 = QGridLayout(self.layoutWidget3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_ip = QLabel(self.layoutWidget3)
        self.label_ip.setObjectName(u"label_ip")
        font3 = QFont()
        font3.setPointSize(20)
        font3.setBold(True)
        font3.setHintingPreference(QFont.PreferDefaultHinting)
        self.label_ip.setFont(font3)

        self.gridLayout_5.addWidget(self.label_ip, 0, 0, 1, 1)

        self.btn_connect = QPushButton(self.layoutWidget3)
        self.btn_connect.setObjectName(u"btn_connect")
        self.btn_connect.setFont(font3)

        self.gridLayout_5.addWidget(self.btn_connect, 0, 2, 1, 1)

        self.edit_ip = QLineEdit(self.layoutWidget3)
        self.edit_ip.setObjectName(u"edit_ip")
        self.edit_ip.setFont(font3)

        self.gridLayout_5.addWidget(self.edit_ip, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(False)
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.edit_ip, self.btn_connect)
        QWidget.setTabOrder(self.btn_connect, self.sb_id_tracking)
        QWidget.setTabOrder(self.sb_id_tracking, self.btn_tracking)
        QWidget.setTabOrder(self.btn_tracking, self.btn_reset_vx)
        QWidget.setTabOrder(self.btn_reset_vx, self.sli_wz)
        QWidget.setTabOrder(self.sli_wz, self.btn_reset_wz)
        QWidget.setTabOrder(self.btn_reset_wz, self.sli_wx)
        QWidget.setTabOrder(self.sli_wx, self.btn_reset_wx)
        QWidget.setTabOrder(self.btn_reset_wx, self.btn_reset_all)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Ch\u01b0\u01a1ng tr\u00ecnh \u0111i\u1ec1u khi\u1ec3n - v1", None))
        self.label_video.setText("")
        self.btn_reset_vx.setText(QCoreApplication.translate("MainWindow", u"M\u1eb7c \u0111\u1ecbnh", None))
        self.label_wz.setText(QCoreApplication.translate("MainWindow", u"\u0110\u1ed9ng c\u01a1 3", None))
        self.btn_reset_wx.setText(QCoreApplication.translate("MainWindow", u"M\u1eb7c \u0111\u1ecbnh", None))
        self.btn_reset_wz.setText(QCoreApplication.translate("MainWindow", u"M\u1eb7c \u0111\u1ecbnh", None))
        self.label_vx.setText(QCoreApplication.translate("MainWindow", u"\u0110\u1ed9ng c\u01a1 1", None))
        self.btn_reset_all.setText(QCoreApplication.translate("MainWindow", u"\u0110\u1eb7t l\u1ea1i m\u1eb7c \u0111\u1ecbnh t\u1ea5t c\u1ea3", None))
        self.label_wx.setText(QCoreApplication.translate("MainWindow", u"\u0110\u1ed9ng c\u01a1 2", None))
        self.btn_save_plot.setText(QCoreApplication.translate("MainWindow", u"Sao l\u01b0u \u0111\u1ed3 th\u1ecb", None))
        self.btn_vx_bw.setText(QCoreApplication.translate("MainWindow", u"L\u00f9i", None))
        self.btn_vx_fw.setText(QCoreApplication.translate("MainWindow", u"Ti\u1ebfn", None))
        self.label_id.setText(QCoreApplication.translate("MainWindow", u"Ch\u1ec9 s\u1ed1 :", None))
        self.btn_tracking.setText(QCoreApplication.translate("MainWindow", u"Theo d\u00f5i", None))
        self.label_count_detect.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_count.setText(QCoreApplication.translate("MainWindow", u"S\u1ed1 l\u01b0\u1ee3ng ph\u00e1t hi\u1ec7n : ", None))
        self.label_ip.setText(QCoreApplication.translate("MainWindow", u"IP :", None))
        self.btn_connect.setText(QCoreApplication.translate("MainWindow", u"K\u1ebft n\u1ed1i", None))
        self.edit_ip.setText(QCoreApplication.translate("MainWindow", u"192.168.88.129:9090", None))
    # retranslateUi

