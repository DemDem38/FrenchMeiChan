import sys 
import os

fc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(fc_path)

from src.noyau_fonctionnel.authentication.person import person

def person_test(print_result = False):

    if print_result:
        print("Execution des tests unitaires de la classe person avec affichage de ce que l'on test")
        print("-"*80)
        print()
        print("Creation d'une personne sans donnees initiales et verification des donnees par defaut")
        print()

    pers1 = person()

    assert pers1.get_last_name(), "X"
    assert pers1.get_first_name(), "x"
    assert pers1.get_birthday(), "00/00/0000"
    assert pers1.get_phone(), "0000000000"
    assert pers1.get_email(), "x@x.x"

    if print_result:
        print()
        print("-"*80)
        print()
        print("Changement des informations de la personne")
        print()

    last_name = "Titi"
    first_name = "Toto"
    birthday = "02/02/2002"
    phone = "0605070809"
    email = "toto.titi@meichan.com"

    pers1.set_last_name(last_name)
    pers1.set_first_name(first_name)
    pers1.set_birthday(birthday)
    pers1.set_phone(phone)
    pers1.set_email(email)

    assert pers1.get_last_name() == last_name
    assert pers1.get_first_name() == first_name
    assert pers1.get_birthday() == birthday
    assert pers1.get_phone() == phone
    assert pers1.get_email() == email

    if print_result:
        print()
        print("-"*80)
        print()
        print("Creation d'une personne avecc des donnees initiales")
        print()

    pers2 = person(last_name, first_name, birthday, phone, email)

    assert pers2.get_last_name() == last_name
    assert pers2.get_first_name() == first_name
    assert pers2.get_birthday() == birthday
    assert pers2.get_phone() == phone
    assert pers2.get_email() == email

    if print_result:
        print()
        print("-"*80)
        print()
        print("Fin des tests")
        print()
        print("-"*80)

if __name__ == "__main__":
    #person_test()
    person_test(print_result = True)
