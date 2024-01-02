import random

def generate_phone():
    phone_number = '89'

    for _ in range(9):
        phone_number += str(random.randint(0, 9))

    return phone_number
