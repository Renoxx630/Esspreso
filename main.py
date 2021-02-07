import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('esspreso.ui', self)
        self.dialog_item_edit = ItemEdit()
        self.connection = sqlite3.connect("coffee.sqlite")
        self.connection.cursor().execute("""CREATE TABLE IF NOT EXISTS coffee(
           id INT PRIMARY KEY,
           name TEXT,
           sort_coffe TEXT,
           stepen TEXT,
           is_molotoy BOOL,
           vkys TEXT,
           coast FLOAT,
           v_upakovki INT);
        """)
        self.connection.commit()
        self.pushButton.clicked.connect(self.select_data)
        self.pushButton_2.clicked.connect(self.show_item_edit)
        # По умолчанию будем выводить все данные из таблицы films
        self.textEdit.setPlainText("SELECT * FROM coffee")
        # self.select_data()

    def show_item_edit(self):
        self.dialog_item_edit.show()

    def select_data(self):
        # Получим результат запроса,
        # который ввели в текстовое поле
        query = self.textEdit.toPlainText()
        res = self.connection.cursor().execute(query).fetchall()
        # Заполним размеры таблицы
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        # При закрытии формы закроем и наше соединение
        # с базой данных
        self.connection.close()


class ItemEdit(QWidget):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("coffee.sqlite")
        uic.loadUi('item.ui', self)
        self.pushButton.clicked.connect(self.add_to_base)

    def add_to_base(self):
        if self.checkBox.isChecked():
            is_molotoy = 'yes'
        else:
            is_molotoy = 'no'
        query = """INSERT INTO coffee(id,
        name,
        sort_coffe,
        stepen,
        is_molotoy,
        vkys,
        coast,
        v_upakovki) 
        VALUES(
        '""" + self.lineEdit.text() + """',
        '""" + self.lineEdit_2.text() + """',
        '""" + self.lineEdit_3.text() + """',
        '""" + self.lineEdit_4.text() + """',
        '""" + is_molotoy + """',
        '""" + self.lineEdit_6.text() + """',
        '""" + self.lineEdit_7.text() + """',
        '""" + self.lineEdit_8.text() + """')
        ;"""

        self.connection.cursor().execute(query)
        # print(query)
        self.connection.commit()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())
