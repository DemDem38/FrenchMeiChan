from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton,QCheckBox, QComboBox, QSpinBox, QDoubleSpinBox

from src.noyau_fonctionnel.authentication.person import person,contact

from src.noyau_fonctionnel.scenario.Scenario import Question, CondAlt

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
        self.textAlt()
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
        self.selectQuestionBox.currentIndexChanged.connect(self.actualiseInfo)
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
        self.selectRobotImage.addItem("Content")
        self.selectRobotImage.addItem("Triste")

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

        self.selectTextAlt.setVisible(b)
        self.selectTimeWidget.setVisible(b)
        self.questionAltTextWidget.setVisible(b)

    def textAlt(self):
        self.textAltWidget = QWidget()
        self.textAltLayout = QHBoxLayout(self.textAltWidget)
        self.textAltLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.textAltWidget)

        self.selectTextAlt = QComboBox()
        self.selectTextAlt.currentIndexChanged.connect(self.actualiseAltInfo)

        self.textAltLayout.addWidget(self.selectTextAlt)

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
        self.createNewQuestion()
        self.addAllQuestions()

    def cancel(self):
        self.parent.mainLayout.setCurrentIndex(0)

    def showCurrentScenarioInformations(self):
        scenario = self.parent.listeScenario[self.parent.combo.currentIndex()]
        id = scenario.getId()

        self.showIDEntry.setText((str)(id))

    def addAllQuestions(self):
        self.selectQuestionBox.clear()
        
        scenario = self.parent.listeScenario[self.parent.combo.currentIndex()]
        listeQuestions = scenario.getListQuestion()
        self.listID = []
        for question in listeQuestions:
            text = question.getTxt()
            self.listID.append(question.getId())
            self.selectQuestionBox.addItem(text)

    def actualiseInfo(self):
        self.selectTextAlt.clear()
        scenario = self.parent.listeScenario[self.parent.combo.currentIndex()]
        id = self.listID[self.selectQuestionBox.currentIndex()]
        question = scenario.getQuestion(id)
        self.showIDEntry.setText((str)(id))
        self.questionTextEntry.setText(question.getTxt())
        self.selectRobotImage.setCurrentIndex(question.getIdRobotFace())

        self.listCond = question.getCondAlt()

        if len(self.listCond) == 0:
            self.checkAltEntry.setChecked(False)
        else:
            self.checkAltEntry.setChecked(True)
            for condALt in self.listCond:
                self.selectTextAlt.addItem(condALt.getTxt())
        
            self.selectTextAlt.adjustSize()


    def actualiseAltInfo(self):
        cond = self.listCond[self.selectTextAlt.currentIndex()]
        listTime = cond.getTime()
        timeMin = listTime[0]
        timeMax = listTime[1]

        self.selectTimeMinEntry.setValue(timeMin)
        self.selectTimeMaxEntry.setValue(timeMax)

        self.questionAltTextEntry.setText(cond.getTxt())

    def resetAllWidget(self):

        self.selectQuestionBox.clear()
        self.showIDEntry.clear()
        self.questionTextEntry.clear()
        self.selectRobotImage.setCurrentIndex(0)
        self.checkAltEntry.setChecked(False)
        self.selectTextAlt.clear()
        self.selectTimeMinEntry.clear()
        self.selectTimeMaxEntry.clear()
        self.questionAltTextEntry.clear()

    def nextID(self):

        scenario = self.parent.listeScenario[self.parent.combo.currentIndex()]
        listeQuestions = scenario.getListQuestion()
        self.listID = []
        maxId = 0
        for question in listeQuestions:
            id = question.getId()
            if id > maxId:
                maxId = id

        newId = maxId + 1
        self.showIDEntry.setText((str)(newId))

    def createNewQuestion(self):
        id = (int) (self.showIDEntry.text())
        text = self.questionTextEntry.text()
        robot = self.selectRobotImage.currentIndex()
        q = Question(id,text, robot)

        if self.checkAltEntry.isChecked():
            mini = self.selectTimeMinEntry.value()
            maxi = self.selectTimeMaxEntry.value()
            txt = self.questionAltTextEntry.text()
            cond = CondAlt(mini,maxi,txt)
            q.addCondTime(cond)
        
        scenario = self.parent.listeScenario[self.parent.combo.currentIndex()]

        scenario.addQuestion(q)
