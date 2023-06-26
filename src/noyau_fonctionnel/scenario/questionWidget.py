from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton,QCheckBox, QComboBox, QSpinBox, QDoubleSpinBox

from src.noyau_fonctionnel.authentication.person import person,contact

class questionWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.parent = parent

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.selectQuestion()
        self.showID()
        self.textEntry()
        self.imageRobot()
        self.checkAlt()
        self.selectTime()
        self.altText()
        self.valideButton()

        self.showAlt()
    def selectQuestion(self):
        self.selectQuestionWidget = QWidget()
        self.selectQuestionLayout = QHBoxLayout(self.selectQuestionWidget)
        self.selectQuestionLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.selectQuestionWidget)

        self.selectQuestionBox = QComboBox()

        self.selectQuestionLayout.addWidget(self.selectQuestionBox)

    def showID(self):
        self.showIDWidget = QWidget()
        self.showIDLayout = QHBoxLayout(self.showIDWidget)
        self.showIDLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.showIDWidget)

        self.showIDPrint = QLabel("ID")

        self.showIDEntry = QLineEdit()
        self.showIDEntry.setReadOnly(True)

        self.showIDLayout.addWidget(self.showIDPrint)
        self.showIDLayout.addWidget(self.showIDEntry)

    def textEntry(self):
        self.questionTextWidget = QWidget()
        self.questionTextLayout = QHBoxLayout(self.questionTextWidget)
        self.questionTextLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.questionTextWidget)

        self.questionTextPrint = QLabel("Texte de la question")

        self.questionTextEntry = QLineEdit()

        self.questionTextLayout.addWidget(self.questionTextPrint)
        self.questionTextLayout.addWidget(self.questionTextEntry)

    def imageRobot(self):
        self.selectRobotImageWidget = QWidget()
        self.selectRobotImageLayout = QHBoxLayout(self.selectRobotImageWidget)
        self.selectRobotImageLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.selectRobotImageWidget)

        self.selectRobotImage = QComboBox()
        self.selectRobotImage.addItem("Normal")
        self.selectRobotImage.addItem("Triste")
        self.selectRobotImage.addItem("Content")

        self.selectRobotImageLayout.addWidget(self.selectRobotImage)
  
    def checkAlt(self):
        self.checkAltWidget = QWidget()
        self.checkAltLayout = QHBoxLayout(self.checkAltWidget)
        self.checkAltLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.checkAltWidget)

        self.checkAltPrint = QLabel("Texte Alternatif")

        self.checkAltEntry = QCheckBox()
        self.checkAltEntry.stateChanged.connect(self.showAlt)
        self.checkAltLayout.addWidget(self.checkAltPrint)
        self.checkAltLayout.addWidget(self.checkAltEntry)

    def showAlt(self):
        b = self.checkAltEntry.isChecked()

        self.selectTimeWidget.setVisible(b)
        self.questionAltTextWidget.setVisible(b)

    def selectTime(self):
        self.selectTimeWidget = QWidget()
        self.selectTimeLayout = QHBoxLayout(self.selectTimeWidget)
        self.selectTimeLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.selectTimeWidget)

        self.selectTimeMinPrint = QLabel("Heure min")

        self.selectTimeMinEntry = QDoubleSpinBox()
        self.selectTimeMinEntry.setDecimals(0)

        self.selectTimeMaxPrint = QLabel("Heure max")

        self.selectTimeMaxEntry = QDoubleSpinBox()
        self.selectTimeMaxEntry.setDecimals(0)

        self.selectTimeLayout.addWidget(self.selectTimeMinPrint)
        self.selectTimeLayout.addWidget(self.selectTimeMinEntry)
        self.selectTimeLayout.addWidget(self.selectTimeMaxPrint)
        self.selectTimeLayout.addWidget(self.selectTimeMaxEntry)
    
    def altText(self):
        self.questionAltTextWidget = QWidget()
        self.questionAltTextLayout = QHBoxLayout(self.questionAltTextWidget)
        self.questionAltTextLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.questionAltTextWidget)

        self.questionAltTextPrint = QLabel("Texte de la question")

        self.questionAltTextEntry = QLineEdit()

        self.questionAltTextLayout.addWidget(self.questionAltTextPrint)
        self.questionAltTextLayout.addWidget(self.questionAltTextEntry)

    def valideButton(self):
        self.valideWidget = QWidget()
        self.valideLayout = QHBoxLayout(self.valideWidget)
        self.valideLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.valideWidget)

        self.validationButton = QPushButton("Valider")
        self.validationButton.released.connect(self.valide)

        self.cancelButton = QPushButton("Retour")
        self.cancelButton.released.connect(self.cancel)

        self.valideLayout.addWidget(self.validationButton)
        self.valideLayout.addWidget(self.cancelButton)

    def valide(self):
        self.addAllQuestions()

    def cancel(self):
        self.parent.mainLayout.setCurrentIndex(0)

    def showCurrentScenarioInformations(self):
        scenario = self.parent.listeScenario[self.parent.combo.currentIndex()]
        id = scenario.getId()

        self.showIDEntry.setText((str)(id))

    def addAllQuestions(self):
        scenario = self.parent.listeScenario[self.parent.combo.currentIndex()]
        listeQuestions = []
        for question in listeQuestions:
            text = question.getTxt()
            self.selectQuestionBox.addItem(text)