from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout
import sqlite3
import sys
from PyQt5 import uic

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.updateButton.clicked.connect(self.default_query)
        self.addButton.clicked.connect(self.add_data)
        self.tableWidget.itemDoubleClicked.connect(self.edit_data)
        self.cur = self.con.cursor()
        self.RowsLst = []
        self.default_query()

    def default_query(self):
        self.query = """ Select * From coffee"""
        data = self.cur.execute(self.query).fetchall()
        self.update_table(data)

    def update_table(self, data):
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            self.RowsLst.append(row)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def add_data(self):
        self.dialog = ChangeCoffee(self.con, self.cur, 'add', None)
        self.dialog.show()

    def edit_data(self):
        row = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        data = self.RowsLst[row[0]]
    #    print(data)

        self.dialog = ChangeCoffee(self.con, self.cur, 'edit', data)
        self.dialog.show()




class ChangeCoffee(QMainWindow):
    def __init__(self, con, cur, action, data):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = con
        self.cur = cur
        self.action = action
        self.data = data
        self.initUI()

    def initUI(self):
        if self.action == 'add':
            self.okButton.clicked.connect(self.add_data)
        if self.action == 'edit':
            self.okButton.clicked.connect(self.edit_data)
            self.lineEdit1.setText(self.data[1])
            self.lineEdit2.setText(self.data[2])
            self.lineEdit3.setText(self.data[3])
            self.lineEdit4.setText(self.data[4])
            self.lineEdit5.setText(str(self.data[5]))
            self.lineEdit6.setText(str(self.data[6]))




    def add_data(self):
        query = f'''insert into coffee(name, roast, type, taste, price, volume)
        values ('{self.lineEdit1.text()}','{self.lineEdit2.text()}','{self.lineEdit3.text()}',
        '{self.lineEdit4.text()}','{self.lineEdit5.text()}','{self.lineEdit6.text()}')'''

        self.cur.execute(query)
        self.con.commit()
        self.close()

    def edit_data(self):
        query = f'''update coffee set (name, roast, type, taste, price, volume) = 
        ('{self.lineEdit1.text()}','{self.lineEdit2.text()}','{self.lineEdit3.text()}',
        '{self.lineEdit4.text()}','{self.lineEdit5.text()}','{self.lineEdit6.text()}')
        where id = {self.data[0]}'''

        self.cur.execute(query)
        self.con.commit()
        self.close()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
