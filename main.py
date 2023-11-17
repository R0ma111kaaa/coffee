import sqlite3
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem

from addEditCoffeeForm import Ui_addEditCoffeeForm
from main_ui import Ui_MainWindow


class Coffee(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.form = None
        self.setupUi(self)
        self.show_info()

        self.addSortButton.clicked.connect(self.addSort)
        self.updateButton.clicked.connect(self.show_info)

        self.tableWidget.cellClicked.connect(self.changeSort)

    def addSort(self):
        self.form = AddSort()
        self.form.show()

    def changeSort(self, row):
        self.tableWidget: QTableWidget
        info = tuple(self.tableWidget.item(row, i).text() for i in range(self.tableWidget.columnCount()))
        self.form = AddSort(info)
        self.form.show()

    def show_info(self):
        self.tableWidget: QTableWidget

        cur = sqlite3.connect("data/coffee.sqlite").cursor()
        response = cur.execute("SELECT * FROM sorts").fetchall()
        if not response:
            return
        self.tableWidget.setColumnCount(len(response[0]))
        self.tableWidget.setRowCount(len(response))
        self.tableWidget.setHorizontalHeaderLabels((i[0] for i in cur.description))
        for i, row in enumerate(response):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))


class AddSort(QMainWindow, Ui_addEditCoffeeForm):
    def __init__(self, info=None):
        super(AddSort, self).__init__()
        self.setupUi(self)

        self.info = info
        self.saveButton.clicked.connect(self.save)

        self.fields = (
            self.lineEdit_1, self.lineEdit_2, self.lineEdit_3,
            self.plainTextEdit, self.lineEdit_4, self.lineEdit_5,
        )

        if info:
            for i in (0, 1, 2, 4, 5):
                elem = info[i + 1]
                self.fields[i].setText(str(elem))
            self.fields[3].setPlainText(info[4])

    def save(self):
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()
        try:
            if self.info:
                cur.execute("UPDATE sorts SET Name=?, roast=?, grain=?, description=?, cost=?, volume=? WHERE id=?",
                            (self.lineEdit_1.text(), int(self.lineEdit_2.text()), int(self.lineEdit_3.text()),
                             self.plainTextEdit.toPlainText(),
                             int(self.lineEdit_4.text()),  int(self.lineEdit_5.text()), self.info[0]))
            else:
                cur.execute(
                    "INSERT INTO sorts (Name, roast, grain, description, cost, volume) VALUES (?, ?, ?, ?, ?, ?)",
                    (self.lineEdit_1.text(), int(self.lineEdit_2.text()), int(self.lineEdit_3.text()),
                        self.plainTextEdit.toPlainText(), int(self.lineEdit_4.text()), int(self.lineEdit_5.text())))
        except sqlite3.IntegrityError:
            self.statusBar().showMessage("Unexpected type")
        else:
            con.commit()
            cur.close()
            con.close()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    c = Coffee()
    c.show()
    sys.exit(app.exec_())
