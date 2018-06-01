import hashlib
import string
from random import *
import secrets


class BaseRandomGenerator:
    def random_string(self):
        pass

    def random_int(self):
        pass


class RandomGenerator(BaseRandomGenerator):
    @staticmethod
    def random_string(min_char = 50, max_char=100):
        characters = string.ascii_letters + string.punctuation + string.digits
        result = "".join(secrets.choice(characters) for x in range(randint(min_char, max_char)))
        result = result.encode('utf-8')
        result = hashlib.sha224(result).hexdigest()
        return result


    @staticmethod
    def random_int(min_char = 5, max_char=12):
        # TODO:: Change function so it reaches min and max of BigInteger of database models.py
        characters = string.digits
        result = "".join(secrets.choice(characters) for x in range(randint(min_char, max_char)))
        return int(result)

