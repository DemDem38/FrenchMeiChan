from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton,QCheckBox, QComboBox, QSpinBox, QDoubleSpinBox

from src.noyau_fonctionnel.authentication.person import person,contact

class reponseWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.parent = parent

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.listeQuestion()
        self.listeReponse()
        self.condition()
        self.previousQuestion()
        self.nextQuestion()
        self.showID()
        self.textEntry()
        self.imageRobot()
        self.checkAlt()
        self.textAlt()
        self.selectTime()
        self.altText()
        self.valideButton()

        self.showAlt()

    def listeQuestion(self):
        self.selectQuestionWidget = QWidget()
        self.selectQuestionLayout = QHBoxLayout(self.selectQuestionWidget)
        self.selectQuestionLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.selectQuestionWidget)

        self.selectQuestionBox = QComboBox()
        self.selectQuestionBox.currentIndexChanged.connect(self.addAllReponse)

        self.selectQuestionLayout.addWidget(self.selectQuestionBox)

    def listeReponse(self):
        self.selectReponseWidget = QWidget()
        self.selectReponseLayout = QHBoxLayout(self.selectReponseWidget)
        self.selectReponseLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.selectReponseWidget)

        self.selectReponseBox = QComboBox()
        self.selectReponseBox.currentIndexChanged.connect(self.actualiseInfo)
        self.selectReponseBox.setFixedWidth(700)

        self.selectReponseLayout.addWidget(self.selectReponseBox)

    def condition(self):
        self.conditionWidget = QWidget()
        self.conditionLayout = QHBoxLayout(self.conditionWidget)
        self.conditionLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.conditionWidget)

        self.conditionPrint = QLabel("Cond")

        self.conditionEntry = QLineEdit()

        self.conditionLayout.addWidget(self.conditionPrint)
        self.conditionLayout.addWidget(self.conditionEntry)

    def previousQuestion(self):
        self.previousQuestionWidget = QWidget()
        self.previousQuestionLayout = QHBoxLayout(self.previousQuestionWidget)
        self.previousQuestionLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.previousQuestionWidget)

        self.previousQuestionPrint = QLabel("Question precedente")

        self.previousQuestionBox = QComboBox()

        self.previousQuestionLayout.addWidget(self.previousQuestionPrint)
        self.previousQuestionLayout.addWidget(self.previousQuestionBox)

    def nextQuestion(self):
        self.nextQuestionWidget = QWidget()
        self.nextQuestionLayout = QHBoxLayout(self.nextQuestionWidget)
        self.nextQuestionLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.nextQuestionWidget)

        self.nextQuestionPrint = QLabel("Question suivante")

        self.nextQuestionBox = QComboBox()

        self.nextQuestionLayout.addWidget(self.nextQuestionPrint)
        self.nextQuestionLayout.addWidget(self.nextQuestionBox)

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
        self.selectTimeMinPrint.setVisible(b)
        self.selectTimeMinEntry.setVisible(b)
        self.selectTimeMaxPrint.setVisible(b)
        self.selectTimeMaxEntry.setVisible(b)
        self.questionAltTextPrint.setVisible(b)
        self.questionAltTextEntry.setVisible(b)

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
        self.addAllQuestions()

    def cancel(self):
        
        self.resetAllWidget()
        self.listID = []
        self.parent.mainLayout.setCurrentIndex(0)

    def addAllQuestions(self):
        self.selectQuestionBox.currentIndexChanged.disconnect(self.addAllReponse)
        self.selectQuestionBox.clear()
        self.previousQuestionBox.clear()
        self.nextQuestionBox.clear()
        
        self.nextQuestionBox.addItem("Pas de question suivante (Fin de Scenario)")

        scenario = self.parent.listeScenario[self.parent.combo.currentIndex()]
        listeQuestions = scenario.getListQuestion()
        self.listID = []
        for question in listeQuestions:
            text = question.getTxt()
            self.listID.append(question.getId())
            self.selectQuestionBox.addItem(text)

            self.previousQuestionBox.addItem(text)
            self.nextQuestionBox.addItem(text)
        self.selectQuestionBox.adjustSize()

        self.selectQuestionBox.currentIndexChanged.connect(self.addAllReponse)
        self.addAllReponse()

    def addAllReponse(self):
        self.selectReponseBox.clear()

        self.previousQuestionBox.setCurrentIndex(self.selectQuestionBox.currentIndex())

        scenario = self.parent.listeScenario[self.parent.combo.currentIndex()]
        id = self.listID[self.selectQuestionBox.currentIndex()]
        question = scenario.getQuestion(id)
        reponses = question.getReponse()

        self.listReponse = []

        for r in reponses:
            self.listReponse.append(r)
            self.selectReponseBox.addItem(r.getTxt())
            
        self.selectReponseBox.adjustSize()
        
    def actualiseInfo(self):
        reponse = self.listReponse[self.selectReponseBox.currentIndex()]

        id = reponse.getId()
        txt = reponse.getTxt()
        cond = reponse.getCond()
        robot = reponse.getIdRobotFace()
        nextQ = reponse.getQuestion()

        if nextQ == None:
            index = 0
        else:
            nextQId = nextQ.getId()
            index = self.listID.index(nextQId) + 1

        self.conditionEntry.setText(self.listToString(cond))
        self.showIDEntry.setText((str)(id))
        self.questionTextEntry.setText(txt)
        self.selectRobotImage.setCurrentIndex(robot)
        self.nextQuestionBox.setCurrentIndex(index)


        self.listCond = reponse.getCondAlt()

        if len(self.listCond) == 0:
            self.checkAltEntry.setChecked(False)
        else:
            self.checkAltEntry.setChecked(True)
            for condALt in self.listCond:
                self.selectTextAlt.addItem(condALt.getTxt())
        
            self.selectTextAlt.adjustSize()

    def listToString(self,list):
        string = ""
        return string
        for i in list:
            for j in i:
                if string == "":
                    string = j
                else:
                    string = string + " / " + j
        
        return string
    
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
        self.selectReponseBox.clear()
        self.showIDEntry.clear()
        self.questionTextEntry.clear()
        self.selectRobotImage.setCurrentIndex(0)
        self.previousQuestionBox.clear()
        self.nextQuestionBox.clear()
        self.checkAltEntry.setChecked(False)
        self.selectTextAlt.clear()
        self.selectTimeMinEntry.clear()
        self.selectTimeMaxEntry.clear()
        self.questionAltTextEntry.clear()