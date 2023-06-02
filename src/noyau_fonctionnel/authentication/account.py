from person import person
import warnings

class account():
    def __init__(self, user, first_contact, other_contacts=[]):
        self.preson = user
        self.first_contact = first_contact
        if other_contacts != []:
            nb_contacts = len(other_contacts)
            if nb_contacts > 4:
                nb_contacts = 4
                warnings.warn("Le nombre maximum de contact est de 5 personnes,\
                              il y en a trop, seulement les 5 premiers seront enregistres")
            for i in range (nb_contacts):
                self["contact"+str(i+2)] = other_contacts[i]
            self.nb_contacts = nb_contacts+1
        else:
            self.nb_contacts = 1

    def get_nb_contacts(self):
        return self.nb_contacts

    def set_new_contact(self, contact):
        if self.nb_contacts == 5:
            warnings.warn("Le nombre maximum de contact est atteint, veuillez en supprimer pour en ajouter un nouveau")
        else:
            self["contact"+str(self.nb_contacts)] = contact
            self.nb_contacts += 1

         # list of persons to contact