import random

def generate_username(email):
    # Take first 25 chars of the string before "@"
    # Then combine with a randomized 5 digit char
    return email.split("@")[0][:25] + str(random.randint(10000, 99999))