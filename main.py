from PyQt5.QtWidgets import *

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from PyQt5.QtCore import QSize, QTimer, pyqtSignal, QEvent, Qt, QObject

from PyQt5.QtGui import QIcon, QPixmap

import sys

import sqlite3

from datetime import datetime

from random import randint



DIGITS = '1234567890'

WORDS = ['Любая', 'Легкая', 'Средняя', 'Тяжелая']


def is_correct_format(text, text_type): # проверка на корректность введенных данных в фильтры Records
    if text_type == 'str_type':
        if text in WORDS:
            return True
        return False
    elif text_type == 'int_type':
        for i in text:
            if i not in DIGITS:
                return False
        return True
    elif text_type == 'date_time_type':
        for i in text:
            if not (i in DIGITS or i == ':'):
                return False
        if ':' in text:
            text = text.split(':')
            if len(text[0]) == len(text[1]) == 2:
                return True
            return False
        return False
    elif text_type == 'date_type':
        for i in text:
            if not (i in DIGITS or i == '-'):
                return False
        if '-' in text:
            year, mounth, day = text.split('-')
            if len(year) == 4:
                if len(mounth) == len(day) == 2:
                    return True
                return False
            return False
        return False


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(920, 660)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(920, 660))
        MainWindow.setMaximumSize(QtCore.QSize(920, 660))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.records_button = QtWidgets.QPushButton(self.centralwidget)
        self.records_button.setGeometry(QtCore.QRect(410, 10, 80, 23))
        self.records_button.setMaximumSize(QtCore.QSize(80, 16777215))
        self.records_button.setStyleSheet("")
        self.records_button.setObjectName("records_button")
        self.help_button = QtWidgets.QPushButton(self.centralwidget)
        self.help_button.setGeometry(QtCore.QRect(500, 10, 80, 23))
        self.help_button.setMaximumSize(QtCore.QSize(80, 23))
        self.help_button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.help_button.setStyleSheet("")
        self.help_button.setObjectName("help_button")
        self.difficult_box = QtWidgets.QComboBox(self.centralwidget)
        self.difficult_box.setGeometry(QtCore.QRect(590, 10, 131, 23))
        self.difficult_box.setMaximumSize(QtCore.QSize(22144, 23))
        self.difficult_box.setStyleSheet("")
        self.difficult_box.setObjectName("difficult_box")
        self.difficult_box.addItem("")
        self.difficult_box.addItem("")
        self.difficult_box.addItem("")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(10, 10, 380, 90))
        self.logo.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.logo.setObjectName("logo")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(620, 40, 91, 61))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.time_l = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.time_l.setObjectName("time_l")
        self.verticalLayout.addWidget(self.time_l)
        self.seconds_lcd = QtWidgets.QLCDNumber(self.verticalLayoutWidget)
        self.seconds_lcd.setMaximumSize(QtCore.QSize(80, 30))
        self.seconds_lcd.setStyleSheet("")
        self.seconds_lcd.setObjectName("seconds_lcd")
        self.verticalLayout.addWidget(self.seconds_lcd)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(410, 40, 101, 61))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.opened_cells_l = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.opened_cells_l.setObjectName("opened_cells_l")
        self.verticalLayout_2.addWidget(self.opened_cells_l)
        self.opened_cells_lcd = QtWidgets.QLCDNumber(self.verticalLayoutWidget_2)
        self.opened_cells_lcd.setEnabled(True)
        self.opened_cells_lcd.setMaximumSize(QtCore.QSize(80, 30))
        self.opened_cells_lcd.setStyleSheet("")
        self.opened_cells_lcd.setObjectName("opened_cells_lcd")
        self.verticalLayout_2.addWidget(self.opened_cells_lcd)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(510, 40, 111, 61))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.flags_l = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.flags_l.setObjectName("flags_l")
        self.verticalLayout_3.addWidget(self.flags_l)
        self.flags_lcd = QtWidgets.QLCDNumber(self.verticalLayoutWidget_3)
        self.flags_lcd.setEnabled(True)
        self.flags_lcd.setMaximumSize(QtCore.QSize(80, 30))
        self.flags_lcd.setStyleSheet("")
        self.flags_lcd.setObjectName("flags_lcd")
        self.verticalLayout_3.addWidget(self.flags_lcd)
        self.results_button = QtWidgets.QPushButton(self.centralwidget)
        self.results_button.setGeometry(QtCore.QRect(730, 74, 80, 26))
        self.results_button.setMaximumSize(QtCore.QSize(80, 16777215))
        self.results_button.setStyleSheet("")
        self.results_button.setObjectName("results_button")
        self.copyright = QtWidgets.QLabel(self.centralwidget)
        self.copyright.setGeometry(QtCore.QRect(730, 10, 111, 21))
        self.copyright.setObjectName("copyright")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 920, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Minesweeper"))
        self.records_button.setText(_translate("MainWindow", "Рекорды"))
        self.help_button.setText(_translate("MainWindow", "Помощь"))
        self.difficult_box.setItemText(0, _translate("MainWindow", "Легкая сложность"))
        self.difficult_box.setItemText(1, _translate("MainWindow", "Средняя сложность"))
        self.difficult_box.setItemText(2, _translate("MainWindow", "Тяжелая сложность"))
        self.logo.setText(_translate("MainWindow", "Minesweeper"))
        self.time_l.setText(_translate("MainWindow", "Время:"))
        self.opened_cells_l.setText(_translate("MainWindow", "Клеток раскрыто:"))
        self.flags_l.setText(_translate("MainWindow", "Флажков осталось:"))
        self.results_button.setText(_translate("MainWindow", "Результаты"))
        self.copyright.setText(_translate("MainWindow", "Ksoksero@yandex.ru"))


class Ui_help_widget(object):
    def setupUi(self, help_widget):
        help_widget.setObjectName("help_widget")
        help_widget.resize(403, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(help_widget.sizePolicy().hasHeightForWidth())
        help_widget.setSizePolicy(sizePolicy)
        help_widget.setMinimumSize(QtCore.QSize(403, 300))
        help_widget.setMaximumSize(QtCore.QSize(2343434, 3434344))
        self.close_button = QtWidgets.QPushButton(help_widget)
        self.close_button.setGeometry(QtCore.QRect(10, 260, 75, 23))
        self.close_button.setObjectName("close_button")
        self.textEdit = QtWidgets.QTextEdit(help_widget)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 380, 241))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMinimumSize(QtCore.QSize(380, 220))
        self.textEdit.setMaximumSize(QtCore.QSize(12334, 234234))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(help_widget)
        QtCore.QMetaObject.connectSlotsByName(help_widget)

    def retranslateUi(self, help_widget):
        _translate = QtCore.QCoreApplication.translate
        help_widget.setWindowTitle(_translate("help_widget", "Помощь"))
        self.close_button.setText(_translate("help_widget", "Закрыть"))
        self.textEdit.setHtml(_translate("help_widget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight"
                                                        ":400; font-style:normal;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block"
                                                        "-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; fo"
                                                        "nt-style:italic; color:"
                                                        "#ffaa00;\">- </span><span style=\" font-size:9pt; font-weight:600; color:#ffaa0"
                                                        "0;\">Игра:</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block"
                                                        "-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Игра начинается, "
                                                        "когда вы нажмете на любую клетку (откроете ее). Цель игры - разминировать все м"
                                                        "ины на игровом поле и открыть все клетки путем нажатия на них. Игра длится до те"
                                                        "х пор, пока вы не разминируете все мины и не откроете все клетки поля или не нат"
                                                        "кнетесь на мину. В игре есть счетчик времени и открытых клеток, с помощью которо"
                                                        "го вы сможете отслеживать свои результаты.</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-"
                                                        "indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">- Выберете сложност"
                                                        "ь под себя:</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-i"
                                                        "ndent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">В игре можно выбрать "
                                                        "сложность. Вы можете играть на &quot;легкой сложности&quot;, &quot;средней сложнос"
                                                        "ти&quot; и &quot;тяжелой сложности&quot;.</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-i"
                                                        "ndent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600; color:#f"
                                                        "faa00;\">- Личные рекорды:</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-ind"
                                                        "ent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">При нажатии а кнопку &quo"
                                                        "t;Рекорды&quot; октрывается окно с таблицей всех ваших сохраненных результатов.</span></p></body></html>"))


class Ui_Records_widget(object):
    def setupUi(self, Records_widget):
        Records_widget.setObjectName("Records_widget")
        Records_widget.resize(842, 589)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Records_widget.sizePolicy().hasHeightForWidth())
        Records_widget.setSizePolicy(sizePolicy)
        Records_widget.setMinimumSize(QtCore.QSize(842, 589))
        Records_widget.setMaximumSize(QtCore.QSize(842, 589))
        self.records_table = QtWidgets.QTableWidget(Records_widget)
        self.records_table.setGeometry(QtCore.QRect(260, 10, 571, 571))
        self.records_table.setObjectName("records_table")
        self.records_table.setColumnCount(5)
        self.records_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.records_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.records_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.records_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.records_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.records_table.setHorizontalHeaderItem(4, item)
        self.filters_l = QtWidgets.QLabel(Records_widget)
        self.filters_l.setGeometry(QtCore.QRect(10, 10, 91, 31))
        self.filters_l.setObjectName("filters_l")
        self.formLayoutWidget = QtWidgets.QWidget(Records_widget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 40, 241, 152))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.date_f_l = QtWidgets.QLabel(self.formLayoutWidget)
        self.date_f_l.setObjectName("date_f_l")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.date_f_l)
        self.time_f_l = QtWidgets.QLabel(self.formLayoutWidget)
        self.time_f_l.setObjectName("time_f_l")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.time_f_l)
        self.time = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.time.setMaximumSize(QtCore.QSize(130, 16777215))
        self.time.setObjectName("time")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.time)
        self.cells_f_l = QtWidgets.QLabel(self.formLayoutWidget)
        self.cells_f_l.setObjectName("cells_f_l")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.cells_f_l)
        self.cells = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.cells.setMaximumSize(QtCore.QSize(130, 16777215))
        self.cells.setObjectName("cells")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cells)
        self.mins_f_l = QtWidgets.QLabel(self.formLayoutWidget)
        self.mins_f_l.setObjectName("mins_f_l")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.mins_f_l)
        self.mins = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.mins.setMaximumSize(QtCore.QSize(130, 16777215))
        self.mins.setObjectName("mins")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.mins)
        self.difficult_f_l = QtWidgets.QLabel(self.formLayoutWidget)
        self.difficult_f_l.setObjectName("difficult_f_l")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.difficult_f_l)
        self.difficult = QtWidgets.QComboBox(self.formLayoutWidget)
        self.difficult.setObjectName("difficult")
        self.difficult.addItem("")
        self.difficult.addItem("")
        self.difficult.addItem("")
        self.difficult.addItem("")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.difficult)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.year = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.year.setMaximumSize(QtCore.QSize(31, 16777215))
        self.year.setText("")
        self.year.setObjectName("year")
        self.horizontalLayout_2.addWidget(self.year)
        self.mounth = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.mounth.setMaximumSize(QtCore.QSize(21, 16777215))
        self.mounth.setText("")
        self.mounth.setObjectName("mounth")
        self.horizontalLayout_2.addWidget(self.mounth)
        self.day = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.day.setMaximumSize(QtCore.QSize(21, 16777215))
        self.day.setText("")
        self.day.setObjectName("day")
        self.horizontalLayout_2.addWidget(self.day)
        self.date_time = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.date_time.setMaximumSize(QtCore.QSize(36, 20))
        self.date_time.setText("")
        self.date_time.setObjectName("date_time")
        self.horizontalLayout_2.addWidget(self.date_time)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.close_button = QtWidgets.QPushButton(Records_widget)
        self.close_button.setGeometry(QtCore.QRect(10, 550, 75, 23))
        self.close_button.setObjectName("close_button")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Records_widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 230, 241, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.load_table_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.load_table_button.setMaximumSize(QtCore.QSize(110, 16777215))
        self.load_table_button.setObjectName("load_table_button")
        self.horizontalLayout.addWidget(self.load_table_button)
        self.reverse_table_box = QtWidgets.QCheckBox(Records_widget)
        self.reverse_table_box.setGeometry(QtCore.QRect(10, 200, 111, 18))
        self.reverse_table_box.setChecked(True)
        self.reverse_table_box.setObjectName("reverse_table_box")
        self.year_mounth_day_time_l = QtWidgets.QLabel(Records_widget)
        self.year_mounth_day_time_l.setGeometry(QtCore.QRect(120, 20, 131, 16))
        self.year_mounth_day_time_l.setObjectName("year_mounth_day_time_l")
        self.delete_data_button = QtWidgets.QPushButton(Records_widget)
        self.delete_data_button.setGeometry(QtCore.QRect(144, 550, 101, 23))
        self.delete_data_button.setStyleSheet("color: rgb(255, 0, 0);")
        self.delete_data_button.setObjectName("delete_data_button")

        self.retranslateUi(Records_widget)
        QtCore.QMetaObject.connectSlotsByName(Records_widget)

    def retranslateUi(self, Records_widget):
        _translate = QtCore.QCoreApplication.translate
        Records_widget.setWindowTitle(_translate("Records_widget", "Таблица рекордов"))
        item = self.records_table.horizontalHeaderItem(0)
        item.setText(_translate("Records_widget", "Дата:"))
        item = self.records_table.horizontalHeaderItem(1)
        item.setText(_translate("Records_widget", "Времени затрачено:"))
        item = self.records_table.horizontalHeaderItem(2)
        item.setText(_translate("Records_widget", "Клеток раскрыто:"))
        item = self.records_table.horizontalHeaderItem(3)
        item.setText(_translate("Records_widget", "Мин разминировано:"))
        item = self.records_table.horizontalHeaderItem(4)
        item.setText(_translate("Records_widget", "На сложности:"))
        self.filters_l.setText(_translate("Records_widget", "<html><head/><body><p><span style=\" font-size:14pt;\">Фильтры:</span></p></body></html>"))
        self.date_f_l.setText(_translate("Records_widget", "Дата:"))
        self.time_f_l.setText(_translate("Records_widget", "Время:"))
        self.cells_f_l.setText(_translate("Records_widget", "Клеток раскрыто:"))
        self.mins_f_l.setText(_translate("Records_widget", "Мин разминировано:"))
        self.difficult_f_l.setText(_translate("Records_widget", "Сложность:"))
        self.difficult.setItemText(0, _translate("Records_widget", "Любая"))
        self.difficult.setItemText(1, _translate("Records_widget", "Легкая"))
        self.difficult.setItemText(2, _translate("Records_widget", "Средняя"))
        self.difficult.setItemText(3, _translate("Records_widget", "Тяжелая"))
        self.close_button.setText(_translate("Records_widget", "Закрыть"))
        self.load_table_button.setText(_translate("Records_widget", "Загрузить данные"))
        self.reverse_table_box.setText(_translate("Records_widget", "Сначала новые"))
        self.year_mounth_day_time_l.setText(_translate("Records_widget", "<html><head/><body><p align=\"center\">год/ месяц/  день  /время</p></body></html>"))
        self.delete_data_button.setText(_translate("Records_widget", "Удалить данные"))


class Ui_SaveResult_widget(object):
    def setupUi(self, SaveResult_widget):
        SaveResult_widget.setObjectName("SaveResult_widget")
        SaveResult_widget.resize(383, 238)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SaveResult_widget.sizePolicy().hasHeightForWidth())
        SaveResult_widget.setSizePolicy(sizePolicy)
        SaveResult_widget.setMinimumSize(QtCore.QSize(383, 238))
        SaveResult_widget.setMaximumSize(QtCore.QSize(383, 238))
        self.verticalLayoutWidget = QtWidgets.QWidget(SaveResult_widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 121, 151))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.time_l = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.time_l.setObjectName("time_l")
        self.verticalLayout.addWidget(self.time_l)
        self.date_l = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.date_l.setObjectName("date_l")
        self.verticalLayout.addWidget(self.date_l)
        self.difficult_l = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.difficult_l.setObjectName("difficult_l")
        self.verticalLayout.addWidget(self.difficult_l)
        self.opened_cells_l = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.opened_cells_l.setObjectName("opened_cells_l")
        self.verticalLayout.addWidget(self.opened_cells_l)
        self.opened_mins_l = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.opened_mins_l.setObjectName("opened_mins_l")
        self.verticalLayout.addWidget(self.opened_mins_l)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(SaveResult_widget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(140, 10, 121, 151))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.time_value_l = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.time_value_l.setObjectName("time_value_l")
        self.verticalLayout_2.addWidget(self.time_value_l)
        self.date_value_l = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.date_value_l.setObjectName("date_value_l")
        self.verticalLayout_2.addWidget(self.date_value_l)
        self.difficult_value_l = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.difficult_value_l.setObjectName("difficult_value_l")
        self.verticalLayout_2.addWidget(self.difficult_value_l)
        self.opened_cells_value_l = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.opened_cells_value_l.setObjectName("opened_cells_value_l")
        self.verticalLayout_2.addWidget(self.opened_cells_value_l)
        self.opened_mins_value_l = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.opened_mins_value_l.setObjectName("opened_mins_value_l")
        self.verticalLayout_2.addWidget(self.opened_mins_value_l)
        self.horizontalLayoutWidget = QtWidgets.QWidget(SaveResult_widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 190, 381, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.save_res_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.save_res_button.setMaximumSize(QtCore.QSize(135, 16777215))
        self.save_res_button.setObjectName("save_res_button")
        self.horizontalLayout.addWidget(self.save_res_button)
        self.dont_save_res_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.dont_save_res_button.setMaximumSize(QtCore.QSize(135, 16777215))
        self.dont_save_res_button.setObjectName("dont_save_res_button")
        self.horizontalLayout.addWidget(self.dont_save_res_button)
        self.line = QtWidgets.QFrame(SaveResult_widget)
        self.line.setGeometry(QtCore.QRect(0, 160, 381, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.win_or_lose_banner = QtWidgets.QLabel(SaveResult_widget)
        self.win_or_lose_banner.setGeometry(QtCore.QRect(160, 170, 158, 16))
        self.win_or_lose_banner.setObjectName("win_or_lose_banner")

        self.retranslateUi(SaveResult_widget)
        QtCore.QMetaObject.connectSlotsByName(SaveResult_widget)

    def retranslateUi(self, SaveResult_widget):
        _translate = QtCore.QCoreApplication.translate
        SaveResult_widget.setWindowTitle(_translate("SaveResult_widget", "Ваш результат"))
        self.time_l.setText(_translate("SaveResult_widget", "Времени затрачено:"))
        self.date_l.setText(_translate("SaveResult_widget", "Дата:"))
        self.difficult_l.setText(_translate("SaveResult_widget", "На сложности:"))
        self.opened_cells_l.setText(_translate("SaveResult_widget", "Клеток раскрыто:"))
        self.opened_mins_l.setText(_translate("SaveResult_widget", "Мин разминировано:"))
        self.time_value_l.setText(_translate("SaveResult_widget", "TextLabel"))
        self.date_value_l.setText(_translate("SaveResult_widget", "TextLabel"))
        self.difficult_value_l.setText(_translate("SaveResult_widget", "TextLabel"))
        self.opened_cells_value_l.setText(_translate("SaveResult_widget", "TextLabel"))
        self.opened_mins_value_l.setText(_translate("SaveResult_widget", "TextLabel"))
        self.save_res_button.setText(_translate("SaveResult_widget", "Сохранить результат"))
        self.dont_save_res_button.setText(_translate("SaveResult_widget", "Не сохранять результат"))
        self.win_or_lose_banner.setText(_translate("SaveResult_widget", "TextLabel"))


class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(400, 170)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(sizePolicy)
        dialog.setMinimumSize(QtCore.QSize(400, 170))
        dialog.setMaximumSize(QtCore.QSize(400, 170))
        self.label = QtWidgets.QLabel(dialog)
        self.label.setGeometry(QtCore.QRect(40, 10, 351, 41))
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 70, 381, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ok_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.ok_button.setMaximumSize(QtCore.QSize(80, 16777215))
        self.ok_button.setAutoDefault(False)
        self.ok_button.setFlat(False)
        self.ok_button.setObjectName("ok_button")
        self.horizontalLayout.addWidget(self.ok_button)
        self.no_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.no_button.setMaximumSize(QtCore.QSize(80, 16777215))
        self.no_button.setAutoDefault(True)
        self.no_button.setDefault(False)
        self.no_button.setObjectName("no_button")
        self.horizontalLayout.addWidget(self.no_button)

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Требуется подтверждение!"))
        self.label.setText(_translate("dialog", "<html><head/><body><p><span style=\" color:#ff0000;\">Вы действительно "
                                                "хотите удалить все данные об резульатах?</span></p></body></html>"))
        self.ok_button.setText(_translate("dialog", "Да"))
        self.no_button.setText(_translate("dialog", "Нет"))


class Dialog(QDialog, Ui_dialog): # появляется, если игрок хочет удалить все данные из БД
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ok_button.clicked.connect(self.deleting)
        self.no_button.clicked.connect(self.deleting)

    def deleting(self): # удаление
        if self.sender().text() == 'Да':
            conn = sqlite3.connect('minesweeper.sqlite')
            cur = conn.cursor()
            data = cur.execute('''DELETE from Records''').fetchall()
            conn.commit()
            conn.close()
        self.close()


class Records(QWidget, Ui_Records_widget): # рекорды
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.opened_dialod = False # открыто ли окно Dialog
        self.filters = {self.time: 'int_type', self.date_time: 'date_time_type', self.year: 'int_type', self.mounth: 'int_type', self.day: 'int_type', self.difficult: 'str_type',
                        self.cells: 'int_type', self.mins: 'int_type'} # фильтры и типы данных каждого из них
        self.year.setPlaceholderText("гггг") # setPlaceholderText - добавление background текста
        self.year.setMaxLength(4)

        self.mounth.setPlaceholderText("мм")
        self.mounth.setMaxLength(2)

        self.day.setPlaceholderText("дд")
        self.day.setMaxLength(2)

        self.date_time.setPlaceholderText("чч:мм")
        self.date_time.setMaxLength(5)

        self.load_table_button.clicked.connect(self.table_filter)
        self.close_button.clicked.connect(self.closeEvent)
        self.delete_data_button.clicked.connect(self.delete_all_data)

    def delete_all_data(self): # открытие окна Dialog
        self.opened_dialod = True
        self.d = Dialog()
        self.d.show()

    def table_filter(self): # сортировка таблицы по фильтрам
        f = [] # сюда добавляются все примененные игроком фильтры
        is_all_succesfully = True # если пройдена проверка is_correct_format()
        for obj in self.filters:
            if obj.objectName() == 'difficult':
                text = obj.currentText()
            else:
                text = obj.text()
            if text != '':
                try:
                    assert is_correct_format(text, self.filters[obj])
                except AssertionError: # введены неверные данные
                    obj.setText('!')
                    is_all_succesfully = False
                else: # все ОК
                    if self.filters[obj] == 'str_type' or self.filters[obj] == 'date_time_type':
                        if text != 'Любая':
                            text = obj.objectName() + ' = ' + '"' + text + '"'
                        else:
                            continue
                    else:
                        text = obj.objectName() + ' = ' + text
                    f.append(text)
        if is_all_succesfully:
            self.load_table(f)

    def load_table(self, f): # загрузка данныз из БД в виджет
        conn = sqlite3.connect('minesweeper.sqlite')
        cur = conn.cursor()
        if len(f) == 0: # если в функции table_filter() в f ничего не добавилось
            f.append('time > -1') # значит нужно отобразить все данные из БД (время всегда больше 0, каким бы не был результат)
        data = cur.execute(f'''SELECT date, time, cells, mins, difficult FROM Records WHERE {' AND '.join(f)}''').fetchall()
        if self.reverse_table_box.isChecked(): # если нужно отсортировать по "новизне"
            data = reversed(data)
        self.records_table.setColumnCount(5)
        self.records_table.setRowCount(0)
        for i, row in enumerate(data):
            self.records_table.setRowCount(self.records_table.rowCount() + 1)
            for j, elem in enumerate(row):
                item = QTableWidgetItem(str(elem))
                item.setFlags(Qt.ItemIsEnabled) # сделаем элемент QTableWidgetItem неизменяемым
                self.records_table.setItem(i, j, item)
        self.records_table.resizeColumnsToContents()
        conn.close()

    def closeEvent(self, event):
        if self.opened_dialod:
            self.d.close()
        self.close()


class Help(QWidget, Ui_help_widget): # окно помощи
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.close_button.clicked.connect(self.closeEvent)

    def closeEvent(self, event):
        self.close()


class SaveResult(QWidget, Ui_SaveResult_widget): # окно сохранения результата
    closed_signal = pyqtSignal(bool) # создается сигнал, с помощью которго потом игра проверяет,
    #                                  закрылось ли окно SaveResult (т.е необходимо перезапустить игру)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = {}
        self.save_res_button.clicked.connect(self.save_res)
        self.dont_save_res_button.clicked.connect(self.closeEvent)

    def save_res(self): # сохранение результата, добавление в БД
        res = '''INSERT INTO Records (date, time, cells, mins, difficult, year, mounth, day, date_time) '''
        res += f'''VALUES ({self.data['date']}, {self.data['time']}, {self.data['cells']}, '''
        res += f'''{self.data['mins']}, {self.data['difficult']},'''
        res += f'''{self.data['year']}, {self.data['mounth']}, {self.data['day']},'''
        res += f'''{self.data['date_time']});'''
        conn = sqlite3.connect('minesweeper.sqlite')
        cur = conn.cursor()
        data = cur.execute(res).fetchall()
        conn.commit()
        conn.close()
        self.closed_signal.emit(True) # тот самый сигнал срабатывает
        self.close()

    def closeEvent(self, event):
        self.closed_signal.emit(True)
        self.close()


class Minesweeper(QMainWindow, Ui_MainWindow): # Main class *******************************************************
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.lose = 1 # Проиграл ли игрок или нет (по умолчанию - проиграл)
        self.game = 0 # Отвечает за процесс игры (игра идет, игра закончилась или перезагружается)
        self.count_of_opened_cells = 0
        self.seconds = 0
        self.count_of_cells = 480
        self.atributes = {} # параметры каждой клетки [клетка] = [роль, (x, y), открыта или нет, под флагом или нет]
        self.coords = {} # [(x, y)] = клетка
        self.difficults = {'Легкая сложность': 40, 'Средняя сложность': 70, 'Тяжелая сложность': 100}
        # -----------------------------------------
        self.opened_help_widget = False
        self.opened_records_widget = False # В этом блоке определяются флаги, обозначющие открыте доп. окна
        self.opened_save_result_widget = False
        # ------------------------------------------
        self.records_button.clicked.connect(self.open_records)
        self.results_button.clicked.connect(self.open_save_result)
        self.help_button.clicked.connect(self.open_help)
        self.results_button.hide()

        self.picture = QPixmap('logo_minesweeper.png')
        self.logo.setPixmap(self.picture)

        y = 110
        for i in range(16):
            x = -20
            y += 30
            for j in range(30):
                x += 30
                self.j = QPushButton('', self)
                self.j.installEventFilter(self)
                self.j.setGeometry(x, y, 30, 30)
                self.coords[(j, i)] = self.j
                self.atributes[self.j] = [None, (j, i), False, False]
                self.j.clicked.connect(self.init_cell)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def init_cell(self): # при клике на cell запускается данная функция
        if self.game == 1: # проверка на стадию игры (игра запущена)
            if not self.atributes[self.sender()][3]: # проверка на "открытость" клетки
                coords = self.atributes[self.sender()][1]
                obj = self.sender()
                role = self.atributes[self.sender()][0]
                self.check_cell(coords, obj, role) # запускаю проверку на "соседей", а также открытие соседних клеток
        elif self.game == 0: # проверка на стадию игры (игра НЕ запущена)
            self.prepare_game(self.sender())

    def check_cell(self, coords, obj, role): # функция-проверка "соседей" и открытие соседних клеток
        if not self.atributes[obj][3]: # если кнопка активна
            if role == 'min':
                self.end_game(coords)
            else:
                self.atributes[obj][2] = True
                obj.setEnabled(False)
                self.count_of_opened_cells += 1
                self.update_count_of_opened_cells(self.count_of_opened_cells)
                x_pos = coords[0]
                y_pos = coords[1]
                count_of_min_in_neighbourhood = 0
                for y in range(y_pos - 1, y_pos + 2):
                    for x in range(x_pos - 1, x_pos + 2):
                        if 0 <= x <= 29:
                            if 0 <= y <= 15:
                                other_obj = self.coords[(x, y)]
                                if self.atributes[other_obj][0] == 'min':
                                    count_of_min_in_neighbourhood += 1
                if count_of_min_in_neighbourhood != 0:
                    obj.setText(str(count_of_min_in_neighbourhood))
                    if self.count_of_opened_cells == self.count_of_cells - self.count_of_mins:
                        self.win()
                else:
                    obj.setText('')
                    for y in range(y_pos - 1, y_pos + 2):
                        for x in range(x_pos - 1, x_pos + 2):
                            if 0 <= x <= 29:
                                if 0 <= y <= 15:
                                    other_obj = self.coords[(x, y)]
                                    if self.atributes[other_obj][0] != 'min':
                                        if self.atributes[other_obj][2] is False:
                                            self.check_cell((x, y), other_obj, 'not_min')

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                self.set_flag(obj)
        return QObject.event(obj, event)

    def set_flag(self, obj): # ставим на клетку флаг
        if self.game == 1:
            if not self.atributes[obj][2]:
                if not self.atributes[obj][3]:
                    if self.count_of_flags != 0:
                        obj.setIcon(QIcon('red_point.png'))
                        obj.setIconSize(QSize(15, 15))
                        self.atributes[obj][3] = True
                        self.count_of_flags -= 1
                        self.update_flags()
                else:
                    obj.setIcon(QIcon())
                    self.atributes[obj][3] = False
                    self.count_of_flags += 1
                    self.update_flags()
    # ---------------------------------------------------------------------------
    # - ниже три функции, отвечающие за обновление дисплеев (таймер, и т.д)

    def update_count_of_opened_cells(self, count):
        self.opened_cells_lcd.display(count)

    def update_timer(self):
        self.seconds += 1
        self.seconds_lcd.display(self.seconds)

    def update_flags(self):
        self.flags_lcd.display(self.count_of_flags)
    # ---------------------------------------------------------------------------

    def prepare_game(self, obj): # подготовка игрового поля
        self.game = 1
        self.seconds = 0
        self.count_of_opened_cells = 0
        self.difficult = self.difficult_box.currentText() # достаю значение сложности
        self.count_of_mins = self.difficults[self.difficult]
        mins = self.difficults[self.difficult] # сколько мин должно быть на данной сложности
        self.count_of_flags = self.difficults[self.difficult] # сколько флажков должно быть на данной сложности
        self.difficult_box.setEnabled(False) # выключаю выбор сложности на время игры
        self.update_flags() # обновляю дисплей количества флажков
        # ----------------------------------------------------
        # раскидываю рандомно мины по полю
        while mins != 0:
            x, y = randint(0, 29), randint(0, 15)
            while self.atributes[self.coords[(x, y)]][0] == 'min':
                x, y = randint(0, 29), randint(0, 15)
            if self.atributes[obj][1] != (x, y):
                self.atributes[self.coords[(x, y)]][0] = 'min'
                mins -= 1
            else:
                self.atributes[obj][0] = 'not_min'
        # -----------------------------------------------------
        coords = self.atributes[obj][1]
        role = self.atributes[obj][0]
        self.timer.start(1000)
        if not self.atributes[obj][3]:
            self.check_cell(coords, obj, role)

    def restart_game(self):
        self.lose = 1
        self.game = 0 # игра в стадии подготовки, еще не запущена
        self.seconds_lcd.display(0)
        self.opened_cells_lcd.display(0)
        self.update_count_of_opened_cells(0)
        # -----------------------------------
        # "чищу" все словари
        for i in self.atributes:
            self.atributes[i][0] = None
            self.atributes[i][2] = False
            self.atributes[i][3] = False
            i.setIcon(QIcon())
            i.setEnabled(True)
            i.setText('')
        self.results_button.hide()

    def end_game(self, coords): # выполнается, если игрок проиграл
        self.game = -1 # игра окончена, проиграна
        self.difficult_box.setEnabled(True) # включаю выбор сложности
        for i in self.atributes:
            if not self.atributes[i][2]:
                if self.atributes[i][0] == 'min': # если мина, ставлю картинку бомбы или взрыва
                    if self.atributes[i][1] == coords:
                        i.setIcon(QIcon('boom_pic.png')) # взрыв, т.к эта клетка была последней открывшейся
                    elif self.atributes[i][3]:
                        i.setIcon(QIcon('bomb_under_flag.png')) # если есть флаг над клеткой
                    else:
                        i.setIcon(QIcon('bomb_pic.png')) # бомба
                    i.setIconSize(QSize(30, 30))
        self.timer.stop() # ZA WARUDO!!! Tomare toki wo
        self.results_button.show()

    def win(self): # если игрок выйграл
        self.lose = 0
        self.game = -1
        self.difficult_box.setEnabled(True)
        for i in self.atributes:
            if not self.atributes[i][2]:
                if self.atributes[i][0] == 'min':
                    i.setIcon(QIcon('bomb_under_flag.png'))
                    i.setIconSize(QSize(30, 30))
        self.count_of_flags = 0
        self.update_flags()
        self.timer.stop()
        self.results_button.show()
    # ------------------------------------------------------------------------------------------
    # далее блок функций, открывающих доп. окна

    def open_records(self):
        self.opened_records_widget = True
        self.r = Records()
        self.r.show()

    def open_help(self):
        self.opened_help_widget = True
        self.h = Help()
        self.h.show()

    def open_save_result(self):
        self.opened_save_result_widget = True
        self.s = SaveResult()
        self.s.show()
        # =================================================
        # задаю значение для каждого label на виджете SaveResult
        self.s.time_value_l.setText(str(self.seconds))

        date = datetime.now()
        date = str(date.strftime('%Y-%m-%d %H:%M:%S'))[:-3]
        year = date.split()[0].split('-')[0]
        mounth = date.split()[0].split('-')[1]
        day = date.split()[0].split('-')[2]
        date_time = date.split()[1]
        diff = self.difficult.split()[0]
        op_cells = self.count_of_opened_cells
        op_mins = self.count_of_mins - self.count_of_flags
        time = self.seconds

        self.s.date_value_l.setText(date)
        self.s.difficult_value_l.setText(diff)
        self.s.opened_cells_value_l.setText(str(op_cells))
        self.s.opened_mins_value_l.setText(str(op_mins))
        self.s.time_value_l.setText(str(time))
        self.s.data = {'date': '"' + date + '"', 'cells': op_cells,
                        'mins': op_mins,
                        'time': time, 'difficult': '"' + diff + '"', 'year': year,
                       'mounth': mounth, 'day': day, 'date_time': '"' + date_time + '"'}
        # ===================================================================================
        if self.lose == 0: # если НЕ проиграл
            self.s.win_or_lose_banner.setText("Вы победили")
        else: # если проиграл
            self.s.win_or_lose_banner.setText("Вы проиграли")
        self.s.closed_signal.connect(self.restart_game) # подключение того самого сигнала к функции
    # ------------------------------------------------------------------------------------------

    def closeEvent(self, event): # закрытие всех окон
        if self.opened_records_widget:
            self.r.close()
        if self.opened_save_result_widget:
            self.s.close()
        if self.opened_help_widget:
            self.h.close()
        self.close()


if '__main__' == __name__:
    app = QApplication(sys.argv)
    ex = Minesweeper()
    ex.show()
    sys.exit(app.exec())
