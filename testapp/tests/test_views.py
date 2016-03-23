# -*- coding:utf-8 -*-
"""Test file for views."""
from testapp.views import entry_view
from testapp.views import home_view
from testapp.models import DBSession, Entry
from pyramid.testing import DummyRequest
import pytest
from webtest import AppError


def test_entry_view_id(dbtransaction, new_model):
    """Test for entry view dictionary title attribute."""
    test_request = DummyRequest()
    test_request.matchdict = {'id': new_model.id}
    dic = entry_view(test_request)
    assert dic['single_entry'].title == 'jill'


def test_entry_view_text(dbtransaction, new_model):
    """Test for entry view dictionary text attribute."""
    test_request = DummyRequest()
    test_request.matchdict = {'id': new_model.id}
    dic = entry_view(test_request)
    assert dic['single_entry'].text == 'jello'


def test_home_view(dbtransaction, new_model):
    """Test home view dictionary title attribute."""
    test_request = DummyRequest()
    dic = home_view(test_request)
    assert dic['entry_list'].all()[0].title == 'jill'


def test_login_route(dbtransaction, app):
    """Test home view dictionary title attribute."""
    response = app.get('/login')
    assert response.status_code == 200


def test_entry_route(dbtransaction, app, new_model):
    """Test home view dictionary title attribute."""
    with pytest.raises(AppError):
        app.get('/entry/{}'.format(new_model.id))


def test_bad_route(dbtransaction, app):
    """Test home view dictionary title attribute."""
    with pytest.raises(AppError):
        app.get('/entry/{}'.format('whatever'))


def test_home_view_sort(dbtransaction, new_model):
    """Test home view sort functionality via attribute."""
    new_model = Entry(title="two", text='twotext')
    DBSession.add(new_model)
    DBSession.flush()
    test_request = DummyRequest()
    dic = home_view(test_request)
    assert dic['entry_list'].all()[1].title == 'jill'


def test_entry_view(dbtransaction, new_model):
    """Test for entry view dictionary is identical to entry instance."""
    test_request = DummyRequest()
    test_request.matchdict = {'id': new_model.id}
    dic = entry_view(test_request)
    assert dic['single_entry'] == new_model
