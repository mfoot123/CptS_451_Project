import sys
import psycopg2
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic, QtCore

# Database connection parameters
DB_NAME = "Milestone1DB"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"

# UI file
qtCreatorFile = "MyUI.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class myApp(QMainWindow):
    def __init__(self):
        super(myApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUI()

    def initUI(self):
        self.connectDB()
        self.populateStates()

        self.ui.stateComboBox.currentIndexChanged.connect(self.populateCities)
        self.ui.cityComboBox.currentIndexChanged.connect(self.populateBusinesses)

    def connectDB(self):
        try:
            self.conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            self.cur = self.conn.cursor()
            print("Connected to database successfully!")
        except Exception as e:
            print("Error connecting to database:", e)

    def populateStates(self):
        self.ui.stateComboBox.clear()
        try:
            self.cur.execute("SELECT DISTINCT state FROM business ORDER BY state;")
            states = self.cur.fetchall()
            for state in states:
                self.ui.stateComboBox.addItem(state[0])
        except Exception as e:
            print("Error fetching states:", e)

    def populateCities(self):
        self.ui.cityComboBox.clear()
        state = self.ui.stateComboBox.currentText()
        try:
            self.cur.execute("SELECT DISTINCT city FROM business WHERE state = %s ORDER BY city;", (state,))
            cities = self.cur.fetchall()
            for city in cities:
                self.ui.cityComboBox.addItem(city[0])
        except Exception as e:
            print("Error fetching cities:", e)

    def populateBusinesses(self):
        self.ui.businessTable.setRowCount(0)
        state = self.ui.stateComboBox.currentText()
        city = self.ui.cityComboBox.currentText()
        try:
            self.cur.execute("SELECT name, city, state FROM business WHERE city = %s AND state = %s ORDER BY name;", (city, state))
            businesses = self.cur.fetchall()
            for row_num, business in enumerate(businesses):
                self.ui.businessTable.insertRow(row_num)
                for col_num, data in enumerate(business):
                    self.ui.businessTable.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        except Exception as e:
            print("Error fetching businesses:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = myApp()
    window.show()
    sys.exit(app.exec_())