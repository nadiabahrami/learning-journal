import os


TEST_DATABASE_URL = 'postgres://nadiabahrami:@localhost:5432/testing'

AUTH_DATA = {'username': 'nadiabahrami', 'password': 'secret'}


def test_password_exist(authenticated_app):
    assert os.environ.get('AUTH_PASSWORD', None) is not None


def test_username_exist(authenticated_app):
    assert os.environ.get('AUTH_USERNAME', None) is not None


def test_check_pw_success(auth_env):
    from testapp.security import check_pw
    password = 'secret'
    assert check_pw(password)


def test_check_pw_fails(auth_env):
    from testapp.security import check_pw
    password = 'banana'
    assert not check_pw(password)


def test_get_login_view(app):
    response = app.get('/')
    assert response.status_code == 200


def test_post_login_success(app):
    response = app.post('/', AUTH_DATA)
    assert response.status_code == 302


def test_post_login_bad_password(app):
    data = {'username': 'nadiabahrami', 'password': 'fails'}
    response = app.post('/', data)
    assert response.status_code == 200


def test_post_login_success_correct_reroute(app):
    response = app.post('/', AUTH_DATA)
    headers = response.headers
    domain = 'http://localhost'
    actual_path = headers.get('Location', "")[len(domain):]
    assert actual_path == '/home'


def test_post_login_success_auth_tkt_present(app, auth_env):
    response = app.post('/', AUTH_DATA)
    headers = response.headers
    cookie_set = headers.getall('Set-Cookie')
    assert cookie_set
    for cookie in cookie_set:
        if cookie.startswith('auth_tkt'):
            break


def test_post_logout_success_auth_tkt_gone(app, auth_env):
    response = app.post('/logout', AUTH_DATA)
    headers = response.headers
    cookie_set = headers.getall('Set-Cookie')
    assert cookie_set
    for cookie in cookie_set:
        if cookie.startswith('auth_tkt'):
            hold = cookie.split(';')
    assert hold[0] == 'auth_tkt='
