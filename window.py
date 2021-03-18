from PySide2.QtWidgets import QWidget, QPushButton, QListWidget, QListWidgetItem, QDesktopWidget, QMessageBox
from PySide2.QtGui import *
from typing import List, Dict
from operator import itemgetter
import PySide2
import main
import sys



class Window(QWidget):
    def __init__(self, data_to_show):
        super().__init__()
        self.data = data_to_show
        self.list_control = None
        self.setGeometry(600, 600, 600, 600)
        self.setup_Window()

    def setup_Window(self):
        self.setWindowTitle("Data Visualizer")
        display_list = QListWidget(self)
        display_list.resize(510,510)
        self.list_control = display_list
        self.add_data_to_list_ascending(self.data)


        visualize_data_button = QPushButton("Visualize Data", self)
        visualize_data_button.move(25, 150)

        update_data_button = QPushButton("Update Data", self)
        update_data_button.move(100, 150)


        self.show()


    def add_data_to_list_ascending(self, data: List[Dict]):
        data.sort(key=itemgetter("More Jobs than Students"))
        for item in data:
            display_text = f"{item['state']}\t\t{item['jobs']}\t\t{item['students']}\t\t{item['More Jobs than Students']}"
            list_item = QListWidgetItem(display_text, listview=self.list_control)
            if item["More Jobs than Students"] < 10:
                list_item.setBackground(QColor('#7fc97f'))
            elif 10 <= item["More Jobs than Students"] < 12:
                list_item.setBackground(QColor('#ffff99'))
            else:
                list_item.setBackground(QColor('#FF3030'))


    def add_data_to_list_descending(self, data: List[Dict]):
        data.sort(key=itemgetter('More Jobs than Students'), reverse=True)
        for item in data:
            display_text = f"{item['state']}\t\t{item['jobs']}\t\t{item['students']}\t\t{item['More Jobs than Students']}"
            list_item = QListWidgetItem(display_text, listview=self.list_control)