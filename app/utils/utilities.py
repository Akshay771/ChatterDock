import random
import string


def generate_unique_string(length=12):
    # Define characters to choose from
    characters = string.ascii_letters + string.digits

    # Generate a random unique string
    unique_string = ''.join(random.choice(characters) for _ in range(length))

    return unique_string

