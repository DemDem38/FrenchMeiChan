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