import sys 
import os

fc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(fc_path)

from PyQt5.QtWidgets import QApplication, QPushButton, QInputDialog, QDesktopWidget, QMainWindow, QComboBox,QStackedLayout, QHBoxLayout, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from src.noyau_fonctionnel.scenario.questionWidget import questionWidget
from src.noyau_fonctionnel.scenario.reponseWidget import reponseWidget

from src.noyau_fonctionnel.scenario.Scenario import ReadScenarioXML,Scenario

class createScenarioWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QStackedLayout(self.mainWidget)

        

        self.widget = QWidget()
        self.mainLayout.addWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)
        self.layout.setAlignment(Qt.AlignCenter)
        
        
        self.addSelectScenario()

        self.addAddButton()

        self.addModifyButton()

        self.questionWidget = questionWidget(self)
        self.reponseWidget = reponseWidget(self)

        self.mainLayout.addWidget(self.questionWidget)
        self.mainLayout.addWidget(self.reponseWidget)

        self.addAllScenario()

    def addSelectScenario(self):
        self.selectScenarioWidget = QWidget()
        self.selectScenarioLayout = QHBoxLayout(self.selectScenarioWidget)
        self.selectScenarioLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.selectScenarioWidget)
        
        self.combo = QComboBox()

        self.addNewButton = QPushButton("Nouveau Scenario")
        self.addNewButton.released.connect(self.get_input_dialog)
        self.addDeleteButton = QPushButton("Delete Scenario")

        self.selectScenarioLayout.addWidget(self.combo)
        self.selectScenarioLayout.addWidget(self.addNewButton)
        self.selectScenarioLayout.addWidget(self.addDeleteButton)
        
    def addAddButton(self):
        self.addScenarioWidget = QWidget()
        self.addScenarioLayout = QHBoxLayout(self.addScenarioWidget)
        self.addScenarioLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.addScenarioWidget)

        self.addQuestionButton = QPushButton("Nouvelle Question")
        self.addQuestionButton.released.connect(self.addQuestion)

        self.addReplyButton = QPushButton("Nouvelle Reponse")
        self.addReplyButton.released.connect(self.addReponse)

        self.addScenarioLayout.addWidget(self.addQuestionButton)
        self.addScenarioLayout.addWidget(self.addReplyButton)

    def addModifyButton(self):
        self.modifyScenarioWidget = QWidget()
        self.modifyScenarioLayout = QHBoxLayout(self.modifyScenarioWidget)
        self.modifyScenarioLayout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.modifyScenarioWidget)

        self.modifyQuestionButton = QPushButton("Modifier Question")
        self.modifyQuestionButton.released.connect(self.modifyQuestion)

        self.modifyReplyButton = QPushButton("Modifier Reponse")
        self.modifyReplyButton.released.connect(self.modifyReponse)

        self.modifyScenarioLayout.addWidget(self.modifyQuestionButton)
        self.modifyScenarioLayout.addWidget(self.modifyReplyButton)

    def addQuestion(self):
        self.questionWidget.selectQuestionWidget.setVisible(False)
        self.questionWidget.resetAllWidget()
        self.questionWidget.nextID()
        self.mainLayout.setCurrentIndex(1)

    def modifyQuestion(self):
        self.questionWidget.selectQuestionWidget.setVisible(True)
        self.questionWidget.showCurrentScenarioInformations()
        self.questionWidget.addAllQuestions()
        self.mainLayout.setCurrentIndex(1)

    def addReponse(self):
        self.mainLayout.setCurrentIndex(2)

    def modifyReponse(self):
        self.reponseWidget.addAllQuestions()
        self.mainLayout.setCurrentIndex(2)
    
    def addAllScenario(self):
        self.listeScenario = ReadScenarioXML("src/noyau_fonctionnel/scenario/listScenario.xml")

        for i in self.listeScenario:
            name = i.getName()
            self.combo.addItem(name)

    def get_input_dialog(self):
        dialog = QInputDialog()
        dialog.setWindowTitle("Entrée de texte")
        dialog.setLabelText("Entrez du texte :")
        if dialog.exec_():
            text = dialog.textValue()
            self.combo.addItem(text)
            scen = Scenario(len(self.listeScenario) + 1,text,[])
            self.listeScenario.append(scen)
            return text
        else:
            return None
        
app = QApplication([])
widget = createScenarioWidget()

screen_geometry = QDesktopWidget().availableGeometry()
widget.resize(screen_geometry.width(), int(0.95 * screen_geometry.height()))

widget.show()
app.exec_()


