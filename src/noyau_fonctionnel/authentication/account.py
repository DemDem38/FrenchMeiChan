#from person import person
from src.noyau_fonctionnel.authentication.person import person, contact
import warnings

class account():
    def __init__(self, user, contacts):
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
