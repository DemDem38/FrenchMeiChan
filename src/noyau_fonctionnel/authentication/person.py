class person():
    def __init__(self, last_name="X", first_name="x", birthday="00/00/0000", phone="0000000000", email="x@x.x"):
        self.last_name = last_name
        self.first_name = first_name
        self.birthday = birthday
        self.phone = phone
        self.email = email

    def get_last_name(self):
        return self.last_name
    def set_last_name(self, last_name):
        self.last_name = last_name

    def get_first_name(self):
        return self.first_name
    def set_first_name(self, first_name):
        self.first_name = first_name

    def get_birthday(self):
        return self.birthday
    def set_birthday(self, birthday):
        self.birthday = birthday

    def get_phone(self):
        return self.phone
    def set_phone(self, phone):
        self.phone = phone

    def get_email(self):
        return self.email
    def set_email(self, email):
        self.email = email

class contact():
    def __init__(self, person, number):
        self.person = person
        self.number = number
    def get_person(self):
        return self.number
    def change_person(self, pers):
        self.person = pers 
    def get_number(self):
        return self.number
    def change_number(self, nb):
        self.number = nb


