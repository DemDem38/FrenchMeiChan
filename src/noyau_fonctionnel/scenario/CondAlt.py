from datetime import datetime

#Classe CondAlt
class CondAlt :
    def __init__(self, min, max, txt) :
        self.tMin = min
        self.tMax = max
        self.txt = txt
        self.next = None
    
    def getTime(self):
        return [self.tMin, self.tMax]

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
