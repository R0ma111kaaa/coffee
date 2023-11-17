import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem


class RandomCircle(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.show_info()

    def show_info(self):
        self.tableWidget: QTableWidget

        cur = sqlite3.connect("coffee.sqlite").cursor()
        response = cur.execute("SELECT * FROM sorts").fetchall()
        if not response:
            return
        self.tableWidget.setColumnCount(len(response[0]))
        self.tableWidget.setRowCount(len(response))
        self.tableWidget.setHorizontalHeaderLabels((i[0] for i in cur.description))
        for i, row in enumerate(response):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rc = RandomCircle()
    rc.show()
    sys.exit(app.exec_())