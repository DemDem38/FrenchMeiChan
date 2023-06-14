from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject, QDate
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QDateEdit, QCalendarWidget, QHBoxLayout,QSpacerItem, QSizePolicy, QVBoxLayout,QTextEdit, QScrollArea, QLabel, QFrame, QGridLayout, QLineEdit, QPushButton, QDesktopWidget
from PyQt5.QtGui import QPixmap, QColor, QKeySequence

from src.noyau_fonctionnel.authentication.account import account
from  src.noyau_fonctionnel.authentication.person import person,contact

class contactWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.parent = parent

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.addChangePersonalInfoWidget()

        self.addContactsWidgets()

        self.returnButton = QPushButton("return")
        self.returnButton.released.connect(self.returnMainWindows)

        self.layout.addWidget(self.returnButton)

    def addChangePersonalInfoWidget(self):
        self.personalInfoWidget = QWidget()
        self.personalInfoLayout = QHBoxLayout(self.personalInfoWidget)
        self.personalInfoLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.personalInfoWidget)
        
        self.changePersonalInfo = QPushButton("Change Personal Information")
        self.changePersonalInfo.released.connect(self.showModifyInformation)
        self.personalInfoLayout.addWidget(self.changePersonalInfo)

    def addContactsWidgets(self):
        self.contactWidget = QWidget()
        self.contactLayout = QHBoxLayout(self.contactWidget)
        self.contactLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.contactWidget)

        self.addContact = QPushButton("Add Contact")
        self.addContact.released.connect(self.showAddContact)

        self.changeContact = QPushButton("Modify Contact")
        self.changeContact.released.connect(self.showModifyContact)

        self.contactLayout.addWidget(self.addContact)
        self.contactLayout.addWidget(self.changeContact)

    def showAddContact(self):
        self.parent.mainLayout.setCurrentIndex(3)

    def showModifyContact(self):
        self.parent.mainLayout.setCurrentIndex(5)

    def showModifyInformation(self):
        personne = self.parent.account.get_user()

        nom = personne.get_last_name()
        prenom = personne.get_first_name()
        date = personne.get_birthday()
        date_format = "dd/MM/yyyy"
        birthday = QDate.fromString(date, date_format)
        phone = personne.get_phone()
        mail = personne.get_email()

        self.parent.userWidget.lastNameEntry.setText(nom)
        self.parent.userWidget.firstNameEntry.setText(prenom)
        self.parent.userWidget.birthdayEntry.setSelectedDate(birthday)
        self.parent.userWidget.phoneEntry.setText(phone)
        self.parent.userWidget.emailEntry.setText(mail)

        self.parent.mainLayout.setCurrentIndex(4)

    def returnMainWindows(self):
        self.parent.mainLayout.setCurrentIndex(0)