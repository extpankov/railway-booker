import random
import string

def generate_email():
    # Characters to include in the email body
    characters = string.ascii_letters + string.digits

    # Generating a random string of 8 characters
    email_body = ''.join(random.choice(characters) for i in range(8))

    # List of possible domains
    domains = ["mail.ru", "yandex.ru", "google.com"]

    # Selecting a random domain
    domain = random.choice(domains)

    # Forming the email address
    email = f"{email_body}@{domain}"

    return email