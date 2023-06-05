from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget,QCheckBox,  QHBoxLayout,QSpacerItem, QSizePolicy, QVBoxLayout,QTextEdit, QScrollArea, QLabel, QFrame, QGridLayout, QLineEdit, QPushButton, QDesktopWidget
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

    def returnMainWindows(self):
        self.parent.mainLayout.setCurrentIndex(0)