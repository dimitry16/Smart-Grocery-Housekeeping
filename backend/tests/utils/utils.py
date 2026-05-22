import random
import string


def random_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=15))


def random_upc() -> str:
    str_random_upc = str(random.randint(10**12, 10**13 - 1))
    return str_random_upc


def random_units() -> str:
    units = ["gallon", "pack", "lb", "grams", "liter", "quart", "loaf", "box"]
    return random.choice(units)
