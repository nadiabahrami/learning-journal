"""Security functions for learning journal."""
import os
from passlib.apps import custom_app_context as pwd_context


def check_pw(pw):
    hashed = pwd_context.encrypt(os.environ.get('AUTH_PASSWORD',
                                                'this is not a password'))
    return pwd_context.verify(pw, hashed)


USERS = {'nadiabahrami': ['g:omnipotent'],
         'viewer': ['viewer']}


def groupfinder(userid, request):
    if userid in USERS:
        return USERS.get(userid, [])
