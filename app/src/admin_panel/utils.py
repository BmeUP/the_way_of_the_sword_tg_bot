import hashlib

from config.settings import settings


def hash_password(password):
    hashed_password = hashlib.sha512((password + settings.salt).encode()).hexdigest()
    return hashed_password


def validate_password(password, hashed_password):
    return hashed_password == hash_password(password)
