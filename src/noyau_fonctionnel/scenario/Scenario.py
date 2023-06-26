import xml.etree.cElementTree as ET
from PyQt5.QtCore import pyqtSignal
from datetime import datetime

#Classe CondAlt
class CondAlt :
    def __init__(self, min, max, txt) :
        self.tMin = min
        self.tMax = max
        self.txt = txt
        self.next = None
    
    def getTime(self):
        return [self.min, self.max]

    #Recupere le texte
    def getTxt(self) :
        return self.txt

    #Ajoute une question suivante alternative
    def addQuestion(self, q):
        self.next = q

    #Retourne la question suivante alternative
    def getQuestion(self) :
        return self.next

    #Retourne l'heure est dans l'intervalle [tMin, tMax[
    def condVrai(self) :
        now = datetime.now()
        time = int(now.strftime("%H"))
        if self.tMin < self.tMax :
            if time >= self.tMin and time < self.tMax :
                return True
        else :
            if time >= self.tMin or time < self.tMax :
                return True
        return False

#Classe Question
class Question :
    def __init__(self, i, s, r) :
        self.id = i
        self.txt = s
        self.robot = r
        self.listeReponse = []
        self.condTime = []
    
    #Recupere l'identifiant
    def getId(self) :
        return self.id
    
    #Recupere le texte
    def getTxt(self) :
        for c in self.condTime :
            if c.condVrai() :
                return c.getTxt()
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
    
    #Ajoute une question alternative
    def addCondTime(self, c) :
        self.condTime.append(c)

    def getCondAlt(self) :
        return self.condTime
    

    #Affiche le texte sur la sortie standard
    def print(self) :
        for c in self.condTime :
            if c.condVrai() :
                print(c.getTxt())
        print(self.txt)

#Classe Reponse
class Reponse :  
    def __init__(self, i,  c,  s, r) :
        self.id = i
        self.cond = c
        self.txt = s
        self.robot = r
        self.questionSuivante = None
        self.condTime = []
        self.nextAlt = None

    #Recupere l'identifiant
    def  getId(self) :
        return self.id

    #Recupere le texte
    def  getTxt(self) :
        self.nextAlt = None
        for c in self.condTime :
            if c.condVrai() :
                self.nextAlt = c
                return c.getTxt()
        return self.txt
    
    #Recupere l'identifiant de la tete du robot
    def getIdRobotFace(self):
        return self.robot
    
    #Pose la question suivante
    def setQuestion(self, q) :
        self.questionSuivante = q
    
    #Recupere la question suivante
    def getQuestion(self) :
        if self.nextAlt != None :
            return self.nextAlt.getQuestion()
        return self.questionSuivante
    
    def getCond(self) :
        return self.cond
    
    def getCondAlt(self) :
        return self.condTime
    
    #Ajoute une reponse altenative
    def addCondTime(self, c) :
        self.condTime.append(c)

    #Affiche le texte sur la sortie standard
    def print(self) :
        self.nextAlt = None
        for c in self.condTime :
            if c.condVrai() :
                self.nextAlt = c
                print(c.getTxt())
        print(self.txt)
    
    #
    def compared(self, s) :
        if self.cond == None :
            return True
        if len(s) >= len(self.cond[0][0]) :
            indice = 0
            for e in s :
                if e.lower() == self.cond[0][0][indice]:
                    indice += 1
                else :
                    indice == 0
                if indice == len(self.cond[0][0]) :
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

def depouperCond(string) :
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
            robotFace = int(q[2].text)
            cond = depouperCond(r[4].text)
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
                if self.listeReponse[i].compared(self.reponse) and rep == 0 :
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
