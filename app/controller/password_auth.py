from app.controller.base_auth import BaseAuth
import re
import json
import os


class PasswordAuth(BaseAuth):

    def __init__(self):
        super().__init__()

    def check_input(self, input):
        email = input.get('email', None)
        err_msg = None

        if email is None or email == '':
            err_msg = 'email cannot be empty'
        elif not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email):
            err_msg = 'wrong email format'

        if err_msg:
            return False, err_msg
        return True, input

    def process_input(self, input):
        return {
            "email": input["email"],
            "type": "password",
            "password": input["password"],
            "username": input["username"],
            "interest1": input["interest1"]
        }
