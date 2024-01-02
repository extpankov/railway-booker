from russian_names import RussianNames
import random
from faker import Faker

class Person:
    def __init__(self, surname, name, lastname, birthdate, gender, passport):
        self.surname = surname
        self.name = name
        self.lastname = lastname
        self.birthdate = birthdate
        self.gender = gender
        self.passport = passport

def generate_person():
    sex = random.choice([0.0, 1.0])
    gender = "male" if sex == 1.0 else "female"
    pr = RussianNames(gender=sex).get_person().split(" ")

    fake = Faker()
    date = fake.date_between(start_date='-18y', end_date='-90y').strftime("%d.%m.%Y")

    pass_serial = int(str(random.randint(11, 78)) + str(random.randint(10, 24)))
    pass_number = random.randint(100000, 999999)
    passport = int(str(pass_serial) + str(pass_number))

    return Person(pr[2], pr[0], pr[1], date, gender, passport)
