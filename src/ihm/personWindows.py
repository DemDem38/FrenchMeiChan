from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QDateEdit, QCalendarWidget, QHBoxLayout,QSpacerItem, QSizePolicy, QVBoxLayout,QTextEdit, QScrollArea, QLabel, QFrame, QGridLayout, QLineEdit, QPushButton, QDesktopWidget
from PyQt5.QtGui import QPixmap, QColor, QKeySequence



class personWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.parent = parent

    def initUI(self):
        self.setWindowTitle('Exemple de widget personnalisé')
        self.setGeometry(200, 200, 300, 200)
        
        self.layout = QVBoxLayout(self)

        self.addLastNameButton()

        self.addFirstNameButton()

        self.addBirthdayWidget()

        self.returnButton = QPushButton("return")
        self.returnButton.pressed.connect(self.returnMainWindows)

        self.layout.addWidget(self.returnButton)

    def addLastNameButton(self):
        self.lastNameWidget = QWidget()
        self.lastNameLayout = QHBoxLayout(self.lastNameWidget)
        self.layout.addWidget(self.lastNameWidget)

        self.lastNamePrint = QLabel("Nom")
        self.lastNameEntry = QLineEdit()

        self.lastNameLayout.addWidget(self.lastNamePrint)
        self.lastNameLayout.addWidget(self.lastNameEntry)
        

    def addFirstNameButton(self):
        self.firstNameWidget = QWidget()
        self.firstNameLayout = QHBoxLayout(self.firstNameWidget)
        self.layout.addWidget(self.firstNameWidget)

        self.firstNamePrint = QLabel("Prenom")
        self.firstNameEntry = QLineEdit()

        self.firstNameLayout.addWidget(self.firstNamePrint)
        self.firstNameLayout.addWidget(self.firstNameEntry)

    def addBirthdayWidget(self):
            self.birthdayWidget = QWidget()
            self.birthdayLayout = QHBoxLayout(self.birthdayWidget)
            self.layout.addWidget(self.birthdayWidget)

            self.birthdayPrint = QLabel("Date de naissance (jj.mm.aaaa)")
            self.birthdayEntry = QCalendarWidget()
            #self.birthdayEntry.setDisplayFormat("dd.MM.yyyy")

            self.birthdayLayout.addWidget(self.birthdayPrint)
            self.birthdayLayout.addWidget(self.birthdayEntry)

    def returnMainWindows(self):
        self.parent.mainLayout.setCurrentIndex(0)