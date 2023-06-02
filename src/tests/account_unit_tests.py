import sys 
import os

fc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(fc_path)

from src.noyau_fonctionnel.authentication.person import person
from src.noyau_fonctionnel.authentication.account import account

user = person("TOTO", "toto", "01/01/2001", "0101010101", "toto@meichan.com")
first_contact = person("TITI", "titi", "02/02/2002", "0202020202", "titi@meichan.com")

acc = account(user, first_contact)

assert acc.user, user
assert acc.first_contact, first_contact
assert acc.nb_contacts, 1

