import sys 
import os

fc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(fc_path)


from src.noyau_fonctionnel.authentication.person import person, contact
import warnings
import json 

class account():
    def __init__(self, user = None, contacts = None):
        if user != None or contacts != None:
            self.user = user
            self.nb_contacts = len(contacts)
            if self.nb_contacts < 1:
                warnings.warn("il faut au ;oins un contact")
            else:
                if self.nb_contacts > 5:
                    self.nb_contacts = 5
                    warnings.warn("Le nombre maximum de contact est de 5 personnes,\
                                il y en a trop, seulement les 5 premiers seront enregistres")
                self.contacts = contacts
                self.check_contacts()
        else:
            json_file = open("data/account.json")
            dict = json.load(json_file)
            self.contacts = []
            for cle, valeur in dict.items():
                if cle == "user":
                    self.user = person(valeur["last name"], valeur["first name"],\
                                       valeur["birthday"], valeur["phone"], valeur["email"])
                else :
                    pers = person(valeur["last name"], valeur["first name"],\
                                       valeur["birthday"], valeur["phone"], valeur["email"])
                    conta = contact(pers, valeur["number"])
                    self.contacts.append(conta)
            self.nb_contacts = len(self.contacts)
            

    def get_nb_contacts(self):
        return self.nb_contacts

    def new_contact(self, contact):
        if self.nb_contacts == 5:
            warnings.warn("Le nombre maximum de contact est atteint, veuillez en supprimer pour en ajouter un nouveau")
        else:
            nb = contact.number
            nb_exist = False
            for i in self.contacts:
                if i.number == nb:
                    warnings.warn("le contact que vous voulez ajouter a un numero deja existant, l'ajout est refuse")
                    nb_exist = True
            if not(nb_exist):
                self.contacts.append(contact)
                self.nb_contacts += 1

    def delete_contact_index(self, index):
        self.contacts.pop(index)
        self.nb_contacts -= 1

    def delete_contact_number(self, no_contact):
        del_contact = False
        for i in self.contacts:
            if i.number == no_contact:
                self.delete_contact(i)
                del_contact = True
        if not(del_contact):
            warnings.warn("Le contact aue vous voulez supprimer n'existe pas")

    def delete_contact(self, contact):
            self.contacts.remove(contact)
            self.nb_contacts -= 1  

    def check_contacts(self):
        list = []
        for i in self.contacts:
            for j in list:
                nb = i.number
                if nb == j:
                    self.delete_contact(i)
                    warnings.warn("Deux conactes ont le meme numero",j,"le second a ete supprime")
                else:
                    list.append(nb)

    def save(self):
        user = {"last name": self.user.last_name, "first name": self.user.first_name, \
                "birthday": self.user.birthday, "phone": self.user.phone, "email": self.user.email}
        account = {"user": user}
        cpt = 1
        for i in self.contacts:
            contact = {"number": i.number, "last name": i.person.last_name,\
                        "first name": i.person.first_name, "birthday": i.person.birthday,\
                        "phone": i.person.phone, "email": i.person.email}
            account["contact"+str(cpt)] = contact
            cpt += 1
        

        with open("data/account.json", "w") as json_file:
            json.dump(account, json_file)

if __name__ == '__main__':
    user = person("TOTO", "toto", "01/01/2001", "0101010101", "toto@meichan.com")
    p1 = person("TITI", "titi", "02/02/2002", "0201020202", "titi@meichan.com")
    c1 = contact(p1, 1)
    acc = account(user, [c1])
    acc.save()

    acc2 = account()


