from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QDateEdit, QCalendarWidget, QHBoxLayout,QSpacerItem, QSizePolicy, QVBoxLayout,QTextEdit, QScrollArea, QLabel, QFrame, QGridLayout, QLineEdit, QPushButton, QDesktopWidget
from PyQt5.QtGui import QPixmap, QColor, QKeySequence

from src.noyau_fonctionnel.authentication.account import account
from  src.noyau_fonctionnel.authentication.person import person,contact

class personalInfoWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.parent = parent

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.addInfoWidget()

        self.addLastNameWidget()

        self.addFirstNameWidget()

        self.addBirthdayWidget()

        self.addPhoneWidget()

        self.addEmailWidget()

        #self.addAddPersonWidget()

        self.addValiderAnnulerWidget()

    def addInfoWidget(self):
        self.infoWidget = QWidget()
        self.infoLayout = QHBoxLayout(self.infoWidget)
        self.infoLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.infoWidget)

        self.infoPrint = QLabel("Bienvenue sur MIC, veuillez renseigner vos informations personnelles")

        font = self.infoPrint.font()
        font.setPointSize(30)
        self.infoPrint.setFont(font)

        self.infoLayout.addWidget(self.infoPrint)

    def addLastNameWidget(self):
        self.lastNameWidget = QWidget()
        self.lastNameLayout = QHBoxLayout(self.lastNameWidget)
        self.lastNameLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.lastNameWidget)

        self.lastNamePrint = QLabel("Nom")
        self.lastNameEntry = QLineEdit()

        self.lastNameLayout.addWidget(self.lastNamePrint)
        self.lastNameLayout.addWidget(self.lastNameEntry)
        

    def addFirstNameWidget(self):
        self.firstNameWidget = QWidget()
        self.firstNameLayout = QHBoxLayout(self.firstNameWidget)
        self.firstNameLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.firstNameWidget)

        self.firstNamePrint = QLabel("Prenom")
        self.firstNameEntry = QLineEdit()

        self.firstNameLayout.addWidget(self.firstNamePrint)
        self.firstNameLayout.addWidget(self.firstNameEntry)

    def addBirthdayWidget(self):
        self.birthdayWidget = QWidget()
        self.birthdayLayout = QHBoxLayout(self.birthdayWidget)
        self.birthdayLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.birthdayWidget)

        self.birthdayPrint = QLabel("Date de naissance (jj.mm.aaaa)")
        self.birthdayEntry = QCalendarWidget()
        self.birthdayEntry.setFixedSize(400, 400)
        #self.birthdayEntry.setDisplayFormat("dd.MM.yyyy")

        self.birthdayLayout.addWidget(self.birthdayPrint)
        self.birthdayLayout.addWidget(self.birthdayEntry)

    def addPhoneWidget(self):
        self.phoneWidget = QWidget()
        self.phoneLayout = QHBoxLayout(self.phoneWidget)
        self.phoneLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.phoneWidget)

        self.phonePrint = QLabel("Numero de telephone")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setMaxLength(10)
        self.phoneEntry.textChanged.connect(self.validatePhoneNumber)
        self.phoneEntry.setReadOnly(False)


        self.phoneLayout.addWidget(self.phonePrint)
        self.phoneLayout.addWidget(self.phoneEntry)

    def addEmailWidget(self):
        self.emailWidget = QWidget()
        self.emailLayout = QHBoxLayout(self.emailWidget)
        self.emailLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.emailWidget)

        self.emailPrint = QLabel("Email")
        self.emailEntry = QLineEdit()

        self.emailLayout.addWidget(self.emailPrint)
        self.emailLayout.addWidget(self.emailEntry)


    def validatePhoneNumber(self, text):
        # Supprimer tous les caractères non numériques
        cleaned_text = ''.join(filter(str.isdigit, text))
        
        if len(cleaned_text) > 10:
            cleaned_text = cleaned_text[:10]  # Limiter le nombre de chiffres à 10
        
        # Mettre à jour le texte du QLineEdit
        self.sender().setText(cleaned_text)

    def addAddPersonWidget(self):
        self.addPersonWidget = QWidget()
        self.addPersonLayout = QHBoxLayout(self.addPersonWidget)
        self.addPersonLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.addPersonWidget)

        self.addPersonPrint = QPushButton("addPerson")

        self.addPersonLayout.addWidget(self.addPersonPrint)

    def addValiderAnnulerWidget(self):
        self.addButtonWidget = QWidget()
        self.addButtonLayout = QHBoxLayout(self.addButtonWidget)
        self.addButtonLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.addButtonWidget)

        self.validerButton = QPushButton("Valider")
        self.validerButton.released.connect(self.validerInfo)

        self.annulerButton = QPushButton("Annuler")
        self.annulerButton.released.connect(self.returnMainWindows)
        self.annulerButton.setVisible(False)

        self.addButtonLayout.addWidget(self.validerButton)
        self.addButtonLayout.addWidget(self.annulerButton)

    def validerInfo(self):
        nom = self. lastNameEntry.text()
        prenom = self.firstNameEntry.text()
        birthday = self.birthdayEntry.selectedDate().toString()
        phone = self.phoneEntry.text()
        email = self.emailEntry.text()
        
        user = person(nom,prenom,birthday,phone,email)
        user2 = person(nom,prenom,birthday,phone,email)
        c1 = contact(user2,1)
        acc = account(user,[c1])
        acc.delete_contact(c1)
        acc.save()
        self.parent.account = acc

        self.returnMainWindows()


    def returnMainWindows(self):
        self.parent.mainLayout.setCurrentIndex(0)
        self.annulerButton.setVisible(True)