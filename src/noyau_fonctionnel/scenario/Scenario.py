import xml.etree.cElementTree as ET

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


listeScenario = ReadScenarioXML("listScenario.xml")
q = listeScenario[1]
#q = init()

print("Bonjour")
reponse = input()

while (q != None) :
    q.print()
    reponse = input()

    listeReponse = q.getReponse()
    rep = 0
    for i in range (len(listeReponse)) :
        if listeReponse[i].compared(reponse) and rep == 0 :
            listeReponse[i].print()
            rep += 1
            q = listeReponse[i].getQuestion()
    if rep == 0 :
        print("Je ne comprend pas")
