import sys 
import os

fc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(fc_path)

from src.noyau_fonctionnel.authentication.person import person, contact
from src.noyau_fonctionnel.authentication.account import account

def account_test(print_result = False):
    if print_result:
        print("Execution des tests unitaires de la classe account avec affichage de ce que l'on test")
        print("-"*80)
        print()
        print("Creation d'une personne et d'un contact dans un compte")
        print()
    user = person("TOTO", "toto", "01/01/2001", "0101010101", "toto@meichan.com")
    first_person = person("TITI", "titi", "02/02/2002", "0202020202", "titi@meichan.com")
    first_contact = contact(first_person, 1)
    if print_result:
        acc = account(user, [first_contact], warning=True)
    else:
        acc = account(user, [first_contact])


    if print_result:
        print()
        print("-"*80)
        print()
        print("Creation d'un compte avec 3 contacts de base")
        print()

    assert acc.user == user
    assert acc.contacts[0] == first_contact
    assert acc.nb_contacts == 1
    
    person2 = person("TUTU", "tutu", "03/03/2003", "0303030303", "tutu@meichan.com")
    person3 = person("TATA", "tata", "04/04/2004", "0404040404", "tata@meichan.com")

    contact2 = contact(person2, 2)
    contact3 = contact(person3, 3)
    if print_result:
        acc = account(user, [first_contact, contact2, contact3], warning=True)
    else:
        acc = account(user, [first_contact, contact2, contact3])


    assert acc.user == user
    assert acc.contacts[0] == first_contact
    assert acc.contacts[1] == contact2
    assert acc.contacts[2] == contact3
    assert acc.nb_contacts == 3

    if print_result:
        print()
        print("-"*80)
        print()
        print("Ajout d'un contact au compte deja cree avec un identifiant deja existant,\n\
un warning devrait apparaitre, l'intentifiant est deja existant")
        print()


    person4 = person("TETE", "tete", "05/05/2005", "0505050505", "tete@meichan.com")
    contact4 = contact(person4, 2)

    acc.new_contact(contact4)
    assert acc.nb_contacts == 3

    if print_result:
        print()
        print("-"*80)
        print()
        print("Ajout de 3 contacts au compte deja cree avec un identifiant deja existant,\n\
un warning devrait apparaitre, il y a un contact de trop a ajouter, max 5 et deja 3 presents")
        print()


    contact4.change_number(4)

    person5 = person("HA", "ha", "06/06/2006", "0606060606", "ha@meichan.com")
    person6 = person("HE", "he", "07/07/2007", "0707070707", "he@meichan.com")
    contact5 = contact(person5, 5)
    contact6 = contact(person6, 6)

    acc.new_contact(contact4)
    acc.new_contact(contact5)
    assert acc.contacts[3] == contact4
    assert acc.contacts[4] == contact5
    assert acc.nb_contacts == 5
    acc.new_contact(contact6)

    if print_result:
        print()
        print("-"*80)
        print()
        print("Suppression de contact par index dans la liste")
        print()

    acc.delete_contact_index(0)
    assert acc.contacts[0] == contact2
    assert acc.contacts[1] == contact3
    assert acc.contacts[2] == contact4
    assert acc.contacts[3] == contact5
    assert acc.nb_contacts == 4

    if print_result:
        print()
        print("-"*80)
        print()
        print("Suppression de contact en donnant le contact lui-meme")
        print()

    acc.delete_contact(contact4)
    assert acc.contacts[0] == contact2
    assert acc.contacts[1] == contact3
    assert acc.contacts[2] == contact5
    assert acc.nb_contacts == 3

    if print_result:
        print()
        print("-"*80)
        print()
        print("Suppression de contact par son numero personnel unique")
        print()

    acc.delete_contact_number(3)
    assert acc.contacts[0] == contact2
    assert acc.contacts[1] == contact5
    assert acc.nb_contacts == 2

    if print_result:
        print()
        print("-"*80)
        print()
        print("Suppression de contact par son numero personnel unique sans que ce numero n'existe\n\
un warning devrait qppqrqitre comme le nomero n'existe pas dans la liste")
        print()

    acc.delete_contact_number(3)

    if print_result:
        print()
        print("-"*80)
        print()
        print("Sauvegarde du compte")
        print()

    acc.save()

    
    if print_result:
        print()
        print("-"*80)
        print()
        print("recuperation du compte sauvegarde et verification des donnees")
        print()


        acc2 = account(warning=True)
    
    else: 
        acc2 = account()

    assert acc.contacts[0].person.last_name == acc2.contacts[0].person.last_name
    assert acc.contacts[0].person.first_name == acc2.contacts[0].person.first_name
    assert acc.contacts[0].person.birthday == acc2.contacts[0].person.birthday
    assert acc.contacts[0].person.phone == acc2.contacts[0].person.phone
    assert acc.contacts[0].person.email == acc2.contacts[0].person.email
    assert acc.contacts[0].number == acc2.contacts[0].number
    assert acc.contacts[1].person.last_name == acc2.contacts[1].person.last_name
    assert acc.contacts[1].person.first_name == acc2.contacts[1].person.first_name
    assert acc.contacts[1].person.birthday == acc2.contacts[1].person.birthday
    assert acc.contacts[1].person.phone == acc2.contacts[1].person.phone
    assert acc.contacts[1].person.email == acc2.contacts[1].person.email
    assert acc.contacts[1].number == acc2.contacts[1].number
    
    if print_result:
        print()
        print("-"*80)
        print()
        print("Fin des tests")
        print()
        print("-"*80)


if __name__ == "__main__":
    account_test()
    #account_test(print_result = True)
