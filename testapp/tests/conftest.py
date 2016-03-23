# -*- coding: utf-8 -*-
import pytest
from sqlalchemy import create_engine
from testapp.models import DBSession, Base, Entry
import os
from testapp import main
from webtest import TestApp
from pyramid.paster import get_appsettings


# TEST_DATABASE_URL = 'sqlite:////tmp/test_db.sqlite'
TEST_DATABASE_URL = 'postgres://nadiabahrami:@localhost:5432/testing'


@pytest.fixture(scope='session')
def config_path():
    """Fixture to send path of dev.ini file."""
    dir_ = os.path.dirname(__file__)
    demo_dir = os.path.join(dir_, '../..')
    return os.path.join(demo_dir, 'nadia_dev.ini')


@pytest.fixture(scope='session')
def test_url():
    """Fixture to access pathe to test database."""
    return TEST_DATABASE_URL


@pytest.fixture(scope='session')
def sqlengine(request):
    engine = create_engine(TEST_DATABASE_URL)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
def dbtransaction(request, sqlengine):
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)
    return connection


@pytest.fixture()
def new_model(request, sqlengine, dbtransaction):
    """Create an entry to testing db."""
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection)
    new_model = Entry(title="jill", text='jello')
    DBSession.add(new_model)
    DBSession.flush()

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)
    return new_model


# This fixture is modified from Will Weatherford github. I don't understand it well.
@pytest.fixture()
def app(config_path, dbtransaction, test_url):
    """Create pretend app fixture of main app to test routing."""
    settings = get_appsettings(config_path)
    settings['sqlalchemy.url'] = test_url
    app = main({}, **settings)
    return TestApp(app)
