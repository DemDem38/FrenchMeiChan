from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton

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

        self.returnButton = QPushButton("Retour")
        self.returnButton.released.connect(self.returnMainWindows)

        self.layout.addWidget(self.returnButton)

    def addChangePersonalInfoWidget(self):
        """
        Ajoute le bouton permettant de switch sur le widget de personalInformation
        """
        self.personalInfoWidget = QWidget()
        self.personalInfoLayout = QHBoxLayout(self.personalInfoWidget)
        self.personalInfoLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.personalInfoWidget)
        
        self.changePersonalInfo = QPushButton("Modifier ses informations")
        self.changePersonalInfo.released.connect(self.showModifyInformation)
        self.personalInfoLayout.addWidget(self.changePersonalInfo)

    def addContactsWidgets(self):
        """
        Ajoute les boutons permettant de switch sur les widgets de addContact et changeContact
        """
        self.contactWidget = QWidget()
        self.contactLayout = QHBoxLayout(self.contactWidget)
        self.contactLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.contactWidget)

        self.addContact = QPushButton("Ajouter un nouveau contact")
        self.addContact.released.connect(self.showAddContact)

        self.changeContact = QPushButton("Modifier un contact existant")
        self.changeContact.released.connect(self.showModifyContact)

        self.contactLayout.addWidget(self.addContact)
        self.contactLayout.addWidget(self.changeContact)

    def showAddContact(self):
        """
        Change la fenetre pour passer sur le widget d'ajout de contact
        """
        self.parent.mainLayout.setCurrentIndex(3)

    def showModifyContact(self):
        """
        Change la fenetre pour passer sur le widget de modification de contact
        """
        self.parent.mainLayout.setCurrentIndex(5)

    def showModifyInformation(self):
        """
        Change la fenetre pour passer sur le widget de changement d'information personel
        """
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
        """
        Change la fenetre pour passer sur le widget principal
        """
        self.parent.mainLayout.setCurrentIndex(0)