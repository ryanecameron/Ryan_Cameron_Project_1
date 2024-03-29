# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window_stacked.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from operator import itemgetter
from typing import List, Dict
from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys, os

import main as main_class
current_database = "collegescorecard.sqlite"


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(650, 450)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")

        self.first_page = QtWidgets.QWidget()
        self.first_page.setObjectName("first_page")

        self.progress_bar = QProgressBar(self.first_page)
        self.progress_bar.setGeometry(QtCore.QRect(50, 400, 550, 15))
        self.progress_bar.hide()

        self.update_data_btn = QtWidgets.QPushButton(self.first_page)
        self.update_data_btn.setGeometry(QtCore.QRect(150, 350, 111, 31))
        self.update_data_btn.setObjectName("update_data_btn")
        self.update_data_btn.clicked.connect(self.update_button_action)

        self.visualize_data_btn = QtWidgets.QPushButton(self.first_page)
        self.visualize_data_btn.setGeometry(QtCore.QRect(350, 350, 111, 31))
        self.visualize_data_btn.setObjectName("visualize_data_btn")
        self.visualize_data_btn.clicked.connect(self.visualize_button_action)
        self.visualizer_button_choice_list = QtWidgets.QRadioButton(self.first_page)
        self.visualizer_button_choice_list.setGeometry(QtCore.QRect(360,400, 111, 31))
        self.visualizer_button_choice_list.setText("LIST")
        self.visualizer_button_choice_list.setChecked(True)
        self.visualizer_button_choice_map = QtWidgets.QRadioButton(self.first_page)
        self.visualizer_button_choice_map.setGeometry(QtCore.QRect(415, 400, 111, 31))
        self.visualizer_button_choice_map.setText("MAP")
        #self.choice_map_label = QtWidgets.QLabel(self.first_page)


        self.stackedWidget.addWidget(self.first_page)
        self.second_page = QtWidgets.QWidget()
        self.second_page.setObjectName("second_page")

        self.descending_button = QtWidgets.QPushButton(self.second_page)
        self.descending_button.setGeometry(QtCore.QRect(20, 400, 101, 31))
        self.descending_button.setObjectName("descending_button")
        self.descending_button.clicked.connect(self.descending_button_action)

        self.home_button_first_page = QtWidgets.QPushButton(self.second_page)
        self.home_button_first_page.setGeometry(QtCore.QRect(500, 400, 101, 31))
        self.home_button_first_page.setText("Home")
        self.home_button_first_page.clicked.connect(self.home_button_action)


        self.listWidget_ascending = QtWidgets.QListWidget(self.second_page)
        self.listWidget_ascending.setGeometry(QtCore.QRect(5, 30, 615, 345))
        self.listWidget_ascending.setObjectName("listWidget")
        self.list_control = self.listWidget_ascending
        self.data = main_class.compare_school_data_with_state_data(current_database)
        self.add_data_to_list(self.data)

        self.label = QtWidgets.QLabel(self.second_page)
        self.label.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.second_page)
        self.label_2.setGeometry(QtCore.QRect(150, 10, 47, 13))
        #self.label_2.setObjectName("label_2")
        self.label_2.setText("Jobs")
        self.label_3 = QtWidgets.QLabel(self.second_page)
        self.label_3.setGeometry(QtCore.QRect(325, 10, 47, 13))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.second_page)
        self.label_4.setGeometry(QtCore.QRect(450, 10, 81, 16))
        self.label_4.setObjectName("label_4")
        self.label_4.setText("Jobs per Student")
        self.stackedWidget.addWidget(self.second_page)

        self.third_page = QtWidgets.QWidget()
        self.third_page.setObjectName("third_page")

        self.home_button_third_page = QtWidgets.QPushButton(self.third_page)
        self.home_button_third_page.setGeometry(QtCore.QRect(500, 400, 101, 31))
        self.home_button_third_page.setText("Home")
        self.home_button_third_page.clicked.connect(self.home_button_action)
        self.ascending_button = QtWidgets.QPushButton(self.third_page)
        self.ascending_button.setGeometry(QtCore.QRect(20, 400, 101, 31))
        self.ascending_button.setObjectName("descending_button")
        self.ascending_button.clicked.connect(self.descending_button_action)


        self.listWidget_descending = QtWidgets.QListWidget(self.third_page)
        self.listWidget_descending.setGeometry(QtCore.QRect(5, 30, 615, 345))
        self.listWidget_descending.setObjectName("listWidget")
        self.third_page_label_state = QtWidgets.QLabel(self.third_page)
        self.third_page_label_state.setText("State")
        self.third_page_label_state.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.third_page_label_jobs = QtWidgets.QLabel(self.third_page)
        self.third_page_label_jobs.setText("Jobs")
        self.third_page_label_jobs.setGeometry(QtCore.QRect(150, 10, 47, 13))
        self.third_page_label_students = QtWidgets.QLabel(self.third_page)
        self.third_page_label_students.setText("Students")
        self.third_page_label_students.setGeometry(QtCore.QRect(325, 10, 47, 13))
        self.third_page_label_jobs_per_student = QtWidgets.QLabel(self.third_page)
        self.third_page_label_jobs_per_student.setText("Jobs Per Student")
        self.third_page_label_jobs_per_student.setGeometry(QtCore.QRect(450, 10, 81, 16))
        self.add_data_to_list_descending(self.data)
        self.stackedWidget.addWidget(self.third_page)

        self.fourth_page = QtWidgets.QWidget()
        #self.fourth_page = QtWebEngineWidgets.QWebEngineView()
        self.fourth_page.setObjectName("fourth_page")
        self.map=QtWebEngineWidgets.QWebEngineView(self.fourth_page)
        self.map.setGeometry(QtCore.QRect(5, 30, 615, 345))
        self.fourth_page_home_button = QtWidgets.QPushButton(self.fourth_page)
        self.fourth_page_home_button.setGeometry(QtCore.QRect(500, 400, 101, 31))
        self.fourth_page_home_button.setText("Home")
        self.fourth_page_home_button.clicked.connect(self.home_button_action)
        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'map.html'))
        fig = main_class.create_map()
        self.map.load(QUrl.fromLocalFile(self.file_path))
        self.stackedWidget.addWidget(self.fourth_page)

        self.verticalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.update_data_btn.setText(_translate("MainWindow", "Update"))
        self.visualize_data_btn.setText(_translate("MainWindow", "Visualize"))
        self.descending_button.setText(_translate("MainWindow", "Descending"))
        self.ascending_button.setText(_translate("MainWindow", "Ascending"))
        self.label.setText(_translate("MainWindow", "State"))
        self.label_2.setText(_translate("MainWindow", "Jobs"))
        self.label_3.setText(_translate("MainWindow", "Students"))
        self.label_4.setText(_translate("MainWindow", "Jobs per Student"))

    def visualize_button_action(self):
        if(self.visualizer_button_choice_list.isChecked()):
            self.stackedWidget.setCurrentIndex(1)
        if(self.visualizer_button_choice_map.isChecked()):
            self.open_map_view()


    def descending_button_action(self):
        self.stackedWidget.setCurrentIndex(2)

    def update_button_action(self):
        self.progress_bar.show()
        main.execute_school_db()
        main.execute_state_db()

    def open_map_view(self):
        self.stackedWidget.setCurrentIndex(3)


    def home_button_action(self):
        self.stackedWidget.setCurrentIndex(0)

    def add_data_to_list(self,data: List[Dict]):
        #data = main.compare_school_data_with_state_data()
        data.sort(key=itemgetter("More Jobs than Students"), reverse=True)
        for item in data:
            display_text = f"{item['state']}\t\t{item['jobs']}\t\t{item['students']}\t\t{item['More Jobs than Students']}"
            list_item = QListWidgetItem(display_text)
            if item["More Jobs than Students"] < 15:
                list_item.setBackground(QColor('#FF3030'))
                self.listWidget_ascending.addItem(list_item)
            elif 15 <= item["More Jobs than Students"] < 18:
                list_item.setBackground(QColor('#ffff99'))
                self.listWidget_ascending.addItem(list_item)
            else:
                list_item.setBackground(QColor('#7fc97f'))
                self.listWidget_ascending.addItem(list_item)

    def add_data_to_list_descending(self, data: List[Dict]):
        data.sort(key=itemgetter("More Jobs than Students"))
        for item in data:
            display_text = f"{item['state']}\t\t{item['jobs']}\t\t{item['students']}\t\t{item['More Jobs than Students']}"
            list_item = QListWidgetItem(display_text)
            if item["More Jobs than Students"] < 10:
                list_item.setBackground(QColor('#FF3030'))
                self.listWidget_descending.addItem(list_item)
            elif 10 <= item["More Jobs than Students"] < 12:
                list_item.setBackground(QColor('#ffff99'))
                self.listWidget_descending.addItem(list_item)
            else:
                list_item.setBackground(QColor('#7fc97f'))
                self.listWidget_descending.addItem(list_item)


if __name__ == "__main__":
    main()


