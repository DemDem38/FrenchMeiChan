import sys 
import os

fc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(fc_path)

from src.noyau_fonctionnel.authentication.person import person, contact
from src.noyau_fonctionnel.authentication.account import account

user = person("TOTO", "toto", "01/01/2001", "0101010101", "toto@meichan.com")
first_contact = person("TITI", "titi", "02/02/2002", "0202020202", "titi@meichan.com")

acc = account(user, first_contact)

assert acc.user == user
assert acc.first_contact == first_contact
assert acc.nb_contacts == 1

person2 = person("TUTU", "tutu", "03/03/2003", "0303030303", "tutu@meichan.com")
person3 = person("TATA", "tata", "04/04/2004", "0404040404", "tata@meichan.com")

contact2 = contact(person2, 2)
contact3 = contact(person3, 3)


acc = account(user, first_contact, [contact2, contact3])

assert acc.user == user
assert acc.first_contact == first_contact
assert acc.other_contacts[0] == contact2
assert acc.other_contacts[1] == contact3
assert acc.nb_contacts == 3

person4 = person("TETE", "tete", "05/05/2005", "0505050505", "tete@meichan.com")
contact4 = contact(person4, 2)

acc.new_contact(contact4)
assert acc.nb_contacts == 3
contact4.change_number(4)

person5 = person("HA", "ha", "06/06/2006", "0606060606", "ha@meichan.com")
person6 = person("HE", "he", "07/07/2007", "0707070707", "he@meichan.com")
contact5 = contact(person5, 5)
contact6 = contact(person6, 6)

acc.new_contact(contact4)
acc.new_contact(contact5)
assert acc.nb_contacts == 5
acc.new_contact(contact6)
