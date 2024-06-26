# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.trade_frame = QtWidgets.QFrame(self.centralwidget)
        self.trade_frame.setGeometry(QtCore.QRect(0, 100, 1200, 700))
        self.trade_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.trade_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.trade_frame.setObjectName("trade_frame")
        self.trade_buttons_frame = QtWidgets.QFrame(self.trade_frame)
        self.trade_buttons_frame.setGeometry(QtCore.QRect(620, 250, 200, 300))
        self.trade_buttons_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.trade_buttons_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.trade_buttons_frame.setObjectName("trade_buttons_frame")
        self.buy_button = QtWidgets.QPushButton(self.trade_buttons_frame)
        self.buy_button.setGeometry(QtCore.QRect(25, 70, 150, 50))
        self.buy_button.setObjectName("buy_button")
        self.step_button = QtWidgets.QPushButton(self.trade_buttons_frame)
        self.step_button.setGeometry(QtCore.QRect(70, 190, 60, 40))
        self.step_button.setObjectName("step_button")
        self.sell_button = QtWidgets.QPushButton(self.trade_buttons_frame)
        self.sell_button.setGeometry(QtCore.QRect(25, 130, 150, 50))
        self.sell_button.setObjectName("sell_button")
        self.trade_log = QtWidgets.QLabel(self.trade_frame)
        self.trade_log.setGeometry(QtCore.QRect(80, 430, 500, 200))
        self.trade_log.setText("")
        self.trade_log.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.trade_log.setObjectName("trade_log")
        self.trade_log_title = QtWidgets.QLabel(self.trade_frame)
        self.trade_log_title.setGeometry(QtCore.QRect(80, 390, 500, 30))
        self.trade_log_title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.trade_log_title.setObjectName("trade_log_title")
        self.trade_options_frame = QtWidgets.QFrame(self.trade_frame)
        self.trade_options_frame.setGeometry(QtCore.QRect(80, 100, 500, 250))
        self.trade_options_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.trade_options_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.trade_options_frame.setObjectName("trade_options_frame")
        self.amt_line_edit = QtWidgets.QLineEdit(self.trade_options_frame)
        self.amt_line_edit.setGeometry(QtCore.QRect(150, 83, 200, 40))
        self.amt_line_edit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.amt_line_edit.setObjectName("amt_line_edit")
        self.call_put_combo_box = QtWidgets.QComboBox(self.trade_options_frame)
        self.call_put_combo_box.setGeometry(QtCore.QRect(200, 143, 100, 25))
        self.call_put_combo_box.setObjectName("call_put_combo_box")
        self.dollar_sign = QtWidgets.QLabel(self.trade_options_frame)
        self.dollar_sign.setGeometry(QtCore.QRect(150, 80, 40, 40))
        self.dollar_sign.setAlignment(QtCore.Qt.AlignCenter)
        self.dollar_sign.setObjectName("dollar_sign")
        self.day_progress_bar = QtWidgets.QProgressBar(self.trade_frame)
        self.day_progress_bar.setGeometry(QtCore.QRect(680, 560, 118, 23))
        self.day_progress_bar.setProperty("value", 24)
        self.day_progress_bar.setObjectName("day_progress_bar")
        self.new_chart_button = QtWidgets.QPushButton(self.trade_frame)
        self.new_chart_button.setGeometry(QtCore.QRect(770, 110, 200, 60))
        self.new_chart_button.setObjectName("new_chart_button")
        self.bought_frame = QtWidgets.QFrame(self.trade_frame)
        self.bought_frame.setGeometry(QtCore.QRect(860, 250, 260, 300))
        self.bought_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bought_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bought_frame.setObjectName("bought_frame")
        self.bought_call_label = QtWidgets.QLabel(self.bought_frame)
        self.bought_call_label.setGeometry(QtCore.QRect(0, 60, 260, 50))
        self.bought_call_label.setAlignment(QtCore.Qt.AlignCenter)
        self.bought_call_label.setObjectName("bought_call_label")
        self.bought_put_label = QtWidgets.QLabel(self.bought_frame)
        self.bought_put_label.setGeometry(QtCore.QRect(0, 130, 260, 50))
        self.bought_put_label.setAlignment(QtCore.Qt.AlignCenter)
        self.bought_put_label.setObjectName("bought_put_label")
        self.bought_invested_label = QtWidgets.QLabel(self.bought_frame)
        self.bought_invested_label.setGeometry(QtCore.QRect(0, 200, 260, 50))
        self.bought_invested_label.setAlignment(QtCore.Qt.AlignCenter)
        self.bought_invested_label.setObjectName("bought_invested_label")
        self.open_chart_button = QtWidgets.QPushButton(self.trade_frame)
        self.open_chart_button.setGeometry(QtCore.QRect(820, 180, 100, 30))
        self.open_chart_button.setObjectName("open_chart_button")
        self.username_label = QtWidgets.QLabel(self.centralwidget)
        self.username_label.setGeometry(QtCore.QRect(25, 25, 500, 50))
        self.username_label.setText("")
        self.username_label.setObjectName("username_label")
        self.money_label = QtWidgets.QLabel(self.centralwidget)
        self.money_label.setGeometry(QtCore.QRect(675, 25, 500, 50))
        self.money_label.setText("")
        self.money_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.money_label.setObjectName("money_label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.buy_button.setText(_translate("MainWindow", "Buy"))
        self.step_button.setText(_translate("MainWindow", "Step"))
        self.sell_button.setText(_translate("MainWindow", "Sell"))
        self.trade_log_title.setText(_translate("MainWindow", "Log:"))
        self.dollar_sign.setText(_translate("MainWindow", "$"))
        self.new_chart_button.setText(_translate("MainWindow", "New Chart"))
        self.bought_call_label.setText(_translate("MainWindow", "Call: $0.0000"))
        self.bought_put_label.setText(_translate("MainWindow", "Put: $0.0000"))
        self.bought_invested_label.setText(_translate("MainWindow", "Invested: $0.0000"))
        self.open_chart_button.setText(_translate("MainWindow", "Open Chart"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
