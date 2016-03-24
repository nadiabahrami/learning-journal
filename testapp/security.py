"""Security functions for learning journal."""
import os
from passlib.apps import custom_app_context as pwd_context
from pyramid.response import Response  # session


def check_pw(pw):
    hashed = pwd_context.encrypt(os.environ.get('AUTH_PASSWORD',
                                                'this is not a password'))
    return pwd_context.verify(pw, hashed)


USERS = {'nadiabahrami': ['g:omnipotent'],
         'viewer': ['viewer']}


def groupfinder(userid, request):
    if userid in USERS:
        return USERS.get(userid, [])


def myview(request):  # session
    session = request.session
    if 'abc' in session:
        session['fred'] = 'yes'
    session['abc'] = '123'
    if 'fred' in session:
        return Response('Fred was in the session')
    else:
        return Response('Fred was not in the session')