# -*- coding: utf-8 -*-
import pytest
from sqlalchemy import create_engine
from testapp.models import DBSession, Base, Entry


TEST_DATABASE_URL = 'sqlite:////tmp/test_db.sqlite'


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
