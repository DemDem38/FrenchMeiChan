import xml.etree.cElementTree as ET
from PyQt5.QtCore import pyqtSignal
from datetime import datetime
import sys 
import os

fc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(fc_path)

from src.noyau_fonctionnel.scenario.CondAlt import CondAlt
from src.noyau_fonctionnel.scenario.Question import Question
from src.noyau_fonctionnel.scenario.Reponse import Reponse
from src.noyau_fonctionnel.language.text_analysis.parse import parse

#Classe Scenario
class Scenario :
    def __init__(self, i,  t,  q) :
        self.id = i
        self.name = t
        self.question = q

    #Recupere l'identifiant
    def  getId(self) :
        return self.id

    #Recupere le nom
    def  getName(self) :
        return self.name

    #Recupere la liste des question du scenario
    def getListQuestion(self) :
        return self.question

    #Recupere la question i du scenario
    def getQuestion(self, i) :
        for q in self.question :
            if q.getId() == i :
                return q
        return None

#Recupere le scenario i de la liste L
def getScenario(L, i) :
    for e in L :
        if e.getId() == i :
            return e
    return None

#Decoupe le string en liste de liste de mot
def decouperCond(string) :
    if (string == None) :
        return None
    listCond = []
    Cond = []
    mot = ''
    for char in string :
        if char == ',' :
            Cond.append(mot)
            mot = ''
        elif char == ';' :
            Cond.append(mot)
            listCond.append(Cond)
            Cond = []
            mot = ''
        elif char != ' ' :
            mot += char
    Cond.append(mot)
    listCond.append(Cond)
    return listCond


#Retourne une liste de scenario a partir de nom de fichier xml
def ReadScenarioXML(name) :
    tree = ET.parse(name)
    root = tree.getroot()
    listeScenario = []

    #Creation des scenarios et des questions
    for e in root :
        idS = int(e[0].text)
        titre = e[1].text
        listeQuestion = []
        #Creation des questions du scenario
        for q in e[2] :
            idQ = int(q[0].text)
            texte = q[1].text
            robotFace = int(q[2].text)
            #Creation de la question
            question = Question(idQ, texte, robotFace)
            
            #Ajout des question alternatives dependant de l'heure
            for c in q[3] :
                min = int(c[0].text)
                max = int(c[1].text)
                txt = c[2].text
                questionAlternative = CondAlt(min, max, txt)
                question.addCondTime(questionAlternative)
            #Ajout de la question a la liste de question du scenario
            listeQuestion.append(question)

        #Creation du scenario
        scenario = Scenario(idS, titre, listeQuestion)
        listeScenario.append(scenario)

    #Parcourt des reponses dans les scenarios
    for e in root :
        #Creation des reponses dans le scenario
        for r in e[3] :
            idR = int(r[0].text)
            texte = r[1].text
            robotFace = int(r[2].text)
            cond = decouperCond(r[4].text)
            #Creation de la reponse
            reponse = Reponse(idR, cond, texte, robotFace)

            #Ajout de la reponse dans la liste de reponse de la question precedente
            scenario = getScenario(listeScenario, int(e[0].text))
            questionPrecedent = scenario.getQuestion(int(r[3].text))
            if questionPrecedent != None :
                questionPrecedent.addReponse(reponse)

            #Ajout de la question suivante a la reponse
            scenarioSuivant = getScenario(listeScenario, int(r[5].text))
            if scenarioSuivant != None :
                questionSuivant = scenarioSuivant.getQuestion(int(r[5][0].text))
                reponse.setQuestion(questionSuivant)

            #Ajout des reponses alternatives dependant de l'heure
            for c in r[6] :
                min = int(c[0].text)
                max = int(c[1].text)
                txt = c[2].text
                questionAlternative = CondAlt(min, max, txt)
                #Ajout de la question suivante a la reponse alternative
                scenarioSuivant = getScenario(listeScenario, int(c[3].text))
                if scenarioSuivant != None :
                    questionSuivant = scenarioSuivant.getQuestion(int(c[3][0].text))
                    questionAlternative.addQuestion(questionSuivant)
                reponse.addCondTime(questionAlternative)
    return listeScenario


class Noyau:
    def __init__(self,IHM):
        self.scenario = 1
        self.ihm = IHM
        self.ihm.signal_envoi_on.connect(self.traiter_string_sound_ON)
        self.ihm.signal_envoi_off.connect(self.traiter_string_sound_OFF)
        self.par = parse()

        self.listeScenario = ReadScenarioXML("src/noyau_fonctionnel/scenario/listScenario.xml")
        self.startScenario(1)

    #Retourne le nombre de scenario
    def numnScenario(self):
        return len(self.listeScenario)

    #Debute le scenario i
    def startScenario(self,i):
        self.scenario = i
        scenario = getScenario(self.listeScenario, i)
        if scenario != None :
            self.q = scenario.getQuestion(1)
            self.ihm.add_left_label(self.q.getTxt())
            self.b = True

    #Retourne l'id du scenario en cours
    def getIDscenario(self):
        return self.scenario

    #
    def traiter_string_sound_ON(self,texte):
        self.traiter_string(texte,speak = True)

    #
    def traiter_string_sound_OFF(self,texte):
        self.traiter_string(texte,speak = False)

    #Analyse texte  a la suite du scenario et repond
    def traiter_string(self, texte, speak = True):
        #Si un scenario est en cours
        if(self.b == True):
            print("Chaîne reçue :", texte)
            self.reponse = texte
            #Recupere les reponse possible
            self.listeReponse = self.q.getReponse()
            rep = 0 
            #Parcours la liste de reponse
            for i in range (len(self.listeReponse)) :
                #Si la condition de la reponse est dans le texte (et que le bot n'a pas repondu)
                if self.listeReponse[i].compared(self.reponse, self.par) and rep == 0 :
                    txt = self.q.getTxt()
                    #Affiche le texte de la reponse s'il existe
                    if txt != None :
                        print(self.listeReponse[i].getTxt())
                        self.ihm.add_left_label(self.listeReponse[i].getTxt(),speak = speak, idImage = self.listeReponse[i].getIdRobotFace())
                    rep += 1
                    #Passe a la question suivante
                    self.q = self.listeReponse[i].getQuestion()
                    #Si on arrive a la fin du scenario
                    if(self.q == None):
                        self.b == False
                        self.ihm.add_left_label("Fin du scenario",speak = speak)
                        self.ihm.toCSV()
                        self.ihm.text_entry.setReadOnly(True)
                        self.ihm.recordBoutton.setEnabled(False)
                    #Si il existe une question suivante
                    else:
                        txt = self.q.getTxt()
                        #Affiche le texte de la question
                        if txt != None :
                            self.ihm.add_left_label(txt,speak = speak, idImage = self.q.getIdRobotFace())
            #Si aucune reponse correct
            if rep == 0 :
                self.ihm.add_left_label("Je ne comprend pas",speak = speak)
