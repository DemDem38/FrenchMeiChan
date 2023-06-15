import xml.etree.cElementTree as ET
from PyQt5.QtCore import pyqtSignal
from datetime import datetime

#Classe Question
class Question :
    def __init__(self, i, s, r) :
        self.id = i
        self.txt = s
        self.robot = r
        self.listeReponse = []
        self.condTime = None
    
    #Recupere l'identifiant
    def getId(self) :
        return self.id
    
    #Recupere le texte
    def getTxt(self) :
        return self.txt

    #Recupere l'identifiant de la tete du robot
    def getIdRobotFace(self):
        return self.robot
    
    #Ajoute une reponse possible a la question
    def addReponse(self, r) :
        self.listeReponse.append(r)

    #Recupere la liste de reponse
    def getReponse(self) :
        return self.listeReponse
    
    #
    def addCondTime(self, min, max) :
        self.condTime = [int(min), int(max)]

    #Affiche le texte sur la sortie standard
    def print(self) :
        print(self.txt)

#Classe Reponse
class Reponse :  
    def __init__(self, i,  c,  s, r) :
        self.id = i
        self.cond = c
        self.txt = s
        self.robot = r
        self.question = None

        self.condTime = None
        self.condTxt = None
        self.condQ = None
        self.bool = False

    #Recupere l'identifiant
    def  getId(self) :
        return self.id

    #Recupere le texte
    def  getTxt(self) :
        return self.txt
    
    #Recupere l'identifiant de la tete du robot
    def getIdRobotFace(self):
        return self.robot
    
    #Pose la question suivante
    def setQuestion(self, q) :
        self.question = q
    
    #Recupere la question suivante
    def getQuestion(self) :
        return self.question
    
    #
    def setCondTxt(self, t) :
        self.condTxt = t

    #
    def addCondTime(self, min, max) :
        self.condTime = [int(min), int(max)]

    #Affiche le texte sur la sortie standard
    def print(self) :
        print(self.getTxt())
    
    #
    def compared(self, s) :
        if self.cond == None :
            return True
        if len(s) >= len(self.cond) :
            indice = 0
            for e in s :
                if e.lower() == self.cond[indice]:
                    indice += 1
                else :
                    indice == 0
                if indice == len(self.cond) -1 :
                    return True
        return False

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
            robotFace = int(q[2].text)
            cond = r[4].text
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
    return listeScenario

def init() :
    q1 = Question(1, "Fait-il chaud aujourd'hui ?")
    q2 = Question(2, "Avez-vous penser a bien vous hydrater ?")
    r1 = Reponse(1, "oui", "Super !", q2)
    r2 = Reponse(2, "non", "Dommage", None)
    r3 = Reponse(3, "oui", "C'est bien, continuer a boire de maniere reguliere", None)
    r4 = Reponse(4, "non", "Penser a boire regulierement", None)
    q1.addReponse(r1)
    q1.addReponse(r2)
    q2.addReponse(r3)
    q2.addReponse(r4)
    return q1
    
class Noyau:
    def __init__(self,IHM):
        self.scenario = 0
        self.ihm = IHM
        self.ihm.signal_envoi_on.connect(self.traiter_string_sound_ON)
        self.ihm.signal_envoi_off.connect(self.traiter_string_sound_OFF)

        self.listeScenario = ReadScenarioXML("src/noyau_fonctionnel/scenario/listScenario.xml")
        self.startScenario(1)

    def numnScenario(self):
        return len(self.listeScenario)

    def startScenario(self,i):
        self.scenario = i
        scenario = getScenario(self.listeScenario, i)
        if scenario != None :
            self.q = scenario.getQuestion(1)
            self.ihm.add_left_label(self.q.getTxt())
            self.b = True

    def getIDscenario(self):
        return self.scenario


    def traiter_string_sound_ON(self,texte):
        self.traiter_string(texte,speak = True)

    def traiter_string_sound_OFF(self,texte):
        self.traiter_string(texte,speak = False)

    def traiter_string(self, texte, speak = True):
        if(self.b == True):
            print("Chaîne reçue :", texte)
            self.reponse = texte
            self.listeReponse = self.q.getReponse()
            rep = 0
            for i in range (len(self.listeReponse)) :
                
                if self.listeReponse[i].compared(self.reponse) and rep == 0 :
                    txt = self.q.getTxt()
                    if txt != None :
                        print(self.listeReponse[i].getTxt())
                        self.ihm.add_left_label(self.listeReponse[i].getTxt(),speak = speak, idImage = self.listeReponse[i].getIdRobotFace())
                    rep += 1
                    self.q = self.listeReponse[i].getQuestion()
                    if(self.q == None):
                        self.b == False
                        self.ihm.add_left_label("Fin du scenario",speak = speak)
                        self.ihm.toCSV()
                        self.ihm.text_entry.setReadOnly(True)
                        self.ihm.recordBoutton.setEnabled(False)
                    else:
                        txt = self.q.getTxt()
                        if txt != None :
                            self.ihm.add_left_label(txt,speak = speak, idImage = self.q.getIdRobotFace())
            if rep == 0 :
                self.ihm.add_left_label("Je ne comprend pas",speak = speak)
