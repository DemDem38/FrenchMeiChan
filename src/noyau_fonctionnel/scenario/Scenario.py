import xml.etree.cElementTree as ET
from PyQt5.QtCore import pyqtSignal
from datetime import datetime

class Question :
    def __init__(self, i, s, r) :
        self.id = i
        self.txt = s
        self.robot = r
        self.listeReponse = []
        self.condTime = None
    
    def getId(self) :
        return self.id
    
    def getTxt(self) :
        return self.txt

    def addReponse(self, r) :
        self.listeReponse.append(r)

    def addCondTime(self, min, max) :
        self.condTime = [int(min), int(max)]

    def getReponse(self) :
        return self.listeReponse

    def print(self) :
        print(self.txt)

class Reponse :  
    def __init__(self, i,  c,  s, q, r) :
        self.id = i
        self.cond = c
        self.txt = s
        self.question = q
        self.robot = r
        self.condTime = None
        self.condTxt = None
        self.condQ = None
        self.bool = False

    
    def  getId(self) :
        return self.id

    def  getTxt(self) :
        if self.condTime != None :
            now = datetime.now()
            current_time = int(now.strftime("%H"))
            if current_time > self.condTime[0] and current_time < self.condTime[1] :
                self.bool = True
                return self.condTxt
        return self.txt
    
    def setTxt(self, t) :
        self.condTxt = t

    def getQuestion(self) :
        if self.bool == True :
            print("Question")
            self.bool = False
            return self.condQ
        return self.question
    
    def setQuestion(self, q) :
        self.condQ = q

    def addCondTime(self, min, max) :
        self.condTime = [int(min), int(max)]
    
    def print(self) :
        print(self.getTxt())
    
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

class Scenario :
    def __init__(self, i,  t,  q) :
        self.id = i
        self.name = t
        self.question = q

    def  getId(self) :
        return self.id

    def  getName(self) :
        return self.name

    def getQuestion(self) :
        return self.question[0]

    def getListQuestion(self) :
        return self.question

def ReadScenarioXML(name) :
    tree = ET.parse(name)
    root = tree.getroot()
    listeScenario = []
    for e in root :
        listeQuestion = []
        for q in e[2] :
            question = Question(q[0].text, q[1].text, q[2].text)
            listeQuestion.append(question)
        for r in e[3] :
            if int(r[4].text) == -1 :
                reponse = Reponse(r[0].text, r[3].text, r[1].text, None,r[5].text)
            else :
                reponse = Reponse(r[0].text, r[3].text, r[1].text, listeQuestion[int(r[4].text) -1], r[5].text)
            if len(r) > 6 :
                time = r[6]
                reponse.addCondTime(time[0].text, time[1].text)
                reponse.setTxt(time[2].text)
                if time[3].text > e[0].text :
                    print("setCondQuestion")
                    reponse.setQuestion(listeScenario[int(time[3].text)-1].getListQuestion()[int(time[4].text)-1])

            listeQuestion[int(r[2].text) -1].addReponse(reponse)

        scenario = Scenario(e[0], e[1], listeQuestion)
        listeScenario.append(scenario)
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
        self.startScenario(0)

    def numnScenario(self):
        return len(self.listeScenario)

    def startScenario(self,i):
        self.scenario = i
        if i < len(self.listeScenario):
            self.q = self.listeScenario[i].getQuestion()
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
                        self.ihm.add_left_label(self.listeReponse[i].getTxt(),speak = speak)
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
                            self.ihm.add_left_label(txt,speak = speak)
            if rep == 0 :
                self.ihm.add_left_label("Je ne comprend pas",speak = speak)
