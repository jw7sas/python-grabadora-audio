from PyQt5.QtWidgets import QWidget, QMessageBox, QLineEdit, QPushButton, QGroupBox, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QGridLayout, QFormLayout, QHBoxLayout, QPlainTextEdit
from PyQt5.QtCore import pyqtSlot, QRect, QSize, Qt
from PyQt5.QtGui import QIcon

class MessageCustom(QMessageBox):
    def __init__(self):
        QMessageBox.__init__(self)
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle("Atención !!")
        self.setText("")
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # self.buttonClicked.connect(self.msgButtonClick)

    def showMessage(self, text):
        self.setText(text)
        self.exec()

    # def msgButtonClick(self, i):
        # print("Button clicked is:",i.text())


class InputCustom(QLineEdit):
    def __init__(self):
        QLineEdit.__init__(self)

    def setValue(self, text):
        self.setText(text)
    
    def getValue(self):
        return self.text()


class ButtonCustom(QPushButton):
    def __init__(self, value="", styles="", param=None, path_icon=None):
        QPushButton.__init__(self, value)
        if path_icon:
            self.setIcon(QIcon(path_icon))
            self.setIconSize(QSize(20,20))

        self.setStyleSheet("{styles}".format(
            styles=styles
        ))
        self.param=param
        self.action=None
        self.clicked.connect(self.clickAction)
        self.setAction()
    
    def clickAction(self):
        if self.action:
            function_string = self.action
            function_string(self.param) if self.param else function_string() 

    def setSize(self, sizeI, sizeE):
        self.setFixedSize(sizeI, sizeE)  

    def setAction(self, action=None):
        if action is not None:
            self.action = action

class BoxInfoCustom(QGroupBox):
    def __init__(self, title):
        QGroupBox.__init__(self, title)
        self.vbox = QVBoxLayout()
        self.textInfo = QPlainTextEdit() 
        self.textInfo.setReadOnly(True)

        self.info = ""
        self.basic_styles = "font-size: 14px; color: black; font-weight: normal; font-family: Helvetica, Arial, sans-serif;"
        self.setInfo()
        self.setLayout(self.vbox)
        self.vbox.addWidget(self.textInfo)
    
    def updateBox(self, info=None, styles=None):
        self.info = "" if info is None else info
        self.basic_styles = self.basic_styles if styles is None else styles
        self.setInfo()

    def cleanBox(self):
        self.textInfo.clear()

    def setInfo(self):
        self.cleanBox()
        self.textInfo.insertPlainText(self.info)
        self.textInfo.setStyleSheet(self.basic_styles)


class MultipleLayoutWidgetCustom(QWidget):
    def __init__(self, elements, parent=None):
        super(MultipleLayoutWidgetCustom, self).__init__(parent)

        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(5)

        # Add elements
        for element in elements:
            layout.addWidget(element)
        
        self.setLayout(layout)


class TableWidgetCustom(QTableWidget):
    def __init__(self):
        QTableWidget.__init__(self)
        self.headers = []
        self.data = []

        self.setHeaders()
        self.setData()
        self.doubleClicked.connect(self.on_click)
        self.move(0,0)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def updateInfoTable(self, headers=None, data=None):
        self.data, self.headers = [], []
        self.headers = [] if headers is None else headers
        self.data = [] if data is None else data
        self.setHeaders()
        self.setData()

    def setHeaders(self):
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)

    def setData(self):
        self.setRowCount(len(self.data))
        for i, values in enumerate(self.data):
            for j, key in enumerate(values):
                try:
                    if key != "methods":
                        self.setItem(i,j, QTableWidgetItem(values[key]))
                    else:
                        methods = values[key]
                        elements = []
                        for method in methods:
                            button = method["button"]
                            button.setAction(method["action"])
                            elements.append(button)

                        self.setCellWidget(i,j, MultipleLayoutWidgetCustom(elements=elements))

                except Exception as e:
                    print(e)