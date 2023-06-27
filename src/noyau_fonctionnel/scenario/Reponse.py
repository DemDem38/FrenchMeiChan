import sys 
import os

fc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(fc_path)
from src.noyau_fonctionnel.language.text_analysis.sentence_analyse import count_same_word

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
    def compared(self, s, parser) :
        if self.cond == None :
            return True
        compteur = 0
        for listCond in self.cond :
            nb = count_same_word(listCond, s, parser)
            if nb > 0 :
                compteur += 1
        if compteur == len(self.cond) :
            return True
        return False

        for c in self.cond[0] :
            if len(s) >= len(c) :
                indice = 0
                for e in s :
                    if e.lower() == c[indice]:
                        indice += 1
                    else :
                        indice == 0
                    if indice == len(c) :
                        return True
        return False