import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestone1App.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone1(QMainWindow):
    def __init__(self):
        super(milestone1, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChange)

    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect("dbname='milestone1db' user ='postgres' host='localhost' password='Asdf123$'")
        except:
            print('Unable to connect to the database')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT distinct state FROM business ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query failed!")  # replace this
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChange(self):
        # clear cities so they don't stack up
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()
        # make sure we are at an index that exists
        if (self.ui.stateList.currentIndex() >= 0):
            sql_str = "SELECT distinct city FROM business WHERE state = '" + state + "' ORDER BY city;"
            try:
                result = self.executeQuery(sql_str)
                for row in result:
                    self.ui.cityList.addItem(row[0])
            except:
                print("No item in row[0] for business in states")

            sql_str = "SELECT name, city, state FROM business WHERE state = '" + state + "' ORDER BY name;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                currentRowCount = 0
                for row in results:
                    for colCount in range (0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query failed!")  # replace this

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone1()
    window.show()
    sys.exit(app.exec_())