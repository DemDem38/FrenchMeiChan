import xml.etree.cElementTree as ET
from PyQt5.QtCore import pyqtSignal

class Question :
    def __init__(self, i, s) :
        self.id = i
        self.txt = s
        self.listeReponse = []
    
    def getId(self) :
        return self.id
    
    def getTxt(self) :
        return self.txt

    def addReponse(self, r) :
        self.listeReponse.append(r)

    def getReponse(self) :
        return self.listeReponse

    def print(self) :
        print(self.txt)

class Reponse :  
    def __init__(self, i,  c,  s, q) :
        self.id = i
        self.cond = c
        self.txt = s
        self.question = q
    
    def  getId(self) :
        return self.id

    def  getTxt(self) :
        return self.txt

    def getQuestion(self) :
        return self.question
    
    def print(self) :
        print(self.txt)
    
    def compared(self, s) :
        indice = 0
        for e in s :
            if e == self.cond[indice]:
                indice += 1
            else :
                indice == 0
            if indice == len(self.cond) -1 :
                return True
        return False

def ReadScenarioXML(name) :
    tree = ET.parse(name)
    root = tree.getroot()
    listeScenario = []
    for e in root :
        listeQuestion = []
        for q in e[0] :
            question = Question(q[0].text, q[1].text)
            listeQuestion.append(question)
        for r in e[1] :
            if int(r[4].text) == -1 :
                reponse = Reponse(r[0].text, r[3].text, r[1].text, None)
            else :
                reponse = Reponse(r[0].text, r[3].text, r[1].text, listeQuestion[int(r[4].text) -1])
            listeQuestion[int(r[2].text) -1].addReponse(reponse)
        listeScenario.append(listeQuestion[0])
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
        self.ihm = IHM
        self.ihm.signal_envoi.connect(self.traiter_string)

        self.listeScenario = ReadScenarioXML("src/noyau_fonctionnel/scenario/listScenario.xml")
        self.q = self.listeScenario[1]
        self.ihm.add_left_label(self.q.getTxt())
        self.b = True
    def traiter_string(self, texte):
        if(self.b == True):
            print("Chaîne reçue :", texte)
            self.reponse = texte
            self.listeReponse = self.q.getReponse()
            rep = 0
            for i in range (len(self.listeReponse)) :
                
                if self.listeReponse[i].compared(self.reponse) and rep == 0 :
                    print(self.listeReponse[i].getTxt())
                    self.ihm.add_left_label(self.listeReponse[i].getTxt())
                    rep += 1
                    self.q = self.listeReponse[i].getQuestion()
                    if(self.q == None):
                        self.b == False
                        self.ihm.add_left_label("Fin du scenario")
                    else:
                        self.ihm.add_left_label(self.q.getTxt())
            if rep == 0 :
                print("Je ne comprend pas")
