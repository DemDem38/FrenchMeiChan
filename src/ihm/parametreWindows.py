from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget,QCheckBox,QColorDialog ,  QHBoxLayout,QSpacerItem, QSizePolicy, QVBoxLayout,QTextEdit, QScrollArea, QLabel, QFrame, QGridLayout, QLineEdit, QPushButton, QDesktopWidget
from PyQt5.QtGui import QPixmap, QColor, QKeySequence



class parametreWidget(QWidget):
    def __init__(self, parent, mainW):
        super().__init__(parent)
        self.initUI()
        self.parent = parent
        self.mainW = mainW

    def initUI(self):
        self.setWindowTitle('Exemple de widget personnalisé')
        self.setGeometry(200, 200, 300, 200)
        
        self.layout = QVBoxLayout(self)

        self.addSaveWidget()
        self.chooseLeftColor()
        self.chooseRightColor()
        self.returnButton = QPushButton("return")
        self.returnButton.pressed.connect(self.returnMainWindows)

        self.layout.addWidget(self.returnButton)

    def addSaveWidget(self):
        self.saveWidget = QWidget()
        self.saveLayout = QHBoxLayout(self.saveWidget)
        self.saveLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.saveWidget)

        self.savePrint = QLabel("Save auto")
        self.saveEntry = QCheckBox()
        self.saveEntry.setChecked(True)

        self.saveLayout.addWidget(self.savePrint)
        self.saveLayout.addWidget(self.saveEntry)

    def chooseLeftColor(self):
        self.leftColorWidget = QWidget()
        self.leftColorLayout = QHBoxLayout(self.leftColorWidget)
        self.leftColorLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.leftColorWidget)

        self.leftColor = "#90EE90"

        self.leftColorPrint = QPushButton("Couleur de gauche")
        self.leftColorEntry = QLabel()
        self.leftColorEntry.setFixedSize(100, 100)
        self.leftColorEntry.setAutoFillBackground(True)
        self.leftColorPrint.pressed.connect(self.changeLeftColor)
        self.leftColorEntry.setStyleSheet("background-color: {}".format(self.leftColor))

        self.leftColorLayout.addWidget(self.leftColorPrint)
        self.leftColorLayout.addWidget(self.leftColorEntry)

    def changeLeftColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.leftColor = color.name()
            self.leftColorEntry.setStyleSheet("background-color: {}".format(self.leftColor))

    def chooseRightColor(self):
        self.rightColorWidget = QWidget()
        self.rightColorLayout = QHBoxLayout(self.rightColorWidget)
        self.rightColorLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.rightColorWidget)

        self.rightColor = "#ADD8E6"

        self.rightColorPrint = QPushButton("Couleur de droite")
        self.rightColorEntry = QLabel()
        self.rightColorEntry.setFixedSize(100, 100)
        self.rightColorEntry.setAutoFillBackground(True)
        self.rightColorPrint.pressed.connect(self.changeRightColor)
        self.rightColorEntry.setStyleSheet("background-color: {}".format(self.rightColor))

        self.rightColorLayout.addWidget(self.rightColorPrint)
        self.rightColorLayout.addWidget(self.rightColorEntry)

    def changeRightColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.rightColor = color.name()
            self.rightColorEntry.setStyleSheet("background-color: {}".format(self.rightColor))

    def returnMainWindows(self):
        self.parent.mainLayout.setCurrentIndex(0)