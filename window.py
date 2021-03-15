from PySide2.QtWidgets import QWidget, QPushButton, QListWidget, QListWidgetItem, QMessageBox
from typing import List, Dict



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
        self.list_control = display_list
        self.add_data_to_list(self.data)
        display_list.resize(590, 525)
        visualize_data_button = QPushButton("Visualize Data", self)
        visualize_data_button.move(100, 550)
        update_data_button = QPushButton("Update Data", self)
        update_data_button.move(200,550)
        self.show()

    def add_data_to_list(self, data: List[Dict]):
        for item in data:
            display_text =f"{item['area_title']}\t\t{item['occ_code']}\t\t{item['occ_title']}\t\t{item['o_group']}" \
                          f"\t\t{item['tot_emp']}\t\t{item['h_pct25']}\t\t{item['a_pct25']}"
            list_item = QListWidgetItem(display_text, listview=self.list_control)



