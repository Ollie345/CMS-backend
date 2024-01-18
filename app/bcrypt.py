
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()  # Create a Bcrypt object


def generate_password_hash(password):
    # Function to generate a password hash
    return bcrypt.generate_password_hash(password).decode('utf-8')


def check_password_hash(password_hash, password):
    # Function to check a password against a hash
    return bcrypt.check_password_hash(password_hash, password)
