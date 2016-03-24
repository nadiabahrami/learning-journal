# -*- coding:utf-8 -*-
"""Test file for views."""
from testapp.views import entry_view
from testapp.views import home_view
from testapp.models import DBSession, Entry
from pyramid.testing import DummyRequest
import pytest
from webtest import AppError


def test_entry_view_title(new_model):
    """Test for entry view dictionary title attribute."""
    test_request = DummyRequest()
    test_request.matchdict = {'id': new_model.id}
    dic = entry_view(test_request)
    assert dic['single_entry'].title == 'jill'


def test_entry_view_text(new_model):
    """Test for entry view dictionary text attribute."""
    test_request = DummyRequest()
    test_request.matchdict = {'id': new_model.id}
    dic = entry_view(test_request)
    assert dic['single_entry'].text == 'jello'


def test_entry_view(new_model):
    """Test for entry view dictionary is identical to entry instance."""
    test_request = DummyRequest()
    test_request.matchdict = {'id': new_model.id}
    dic = entry_view(test_request)
    assert dic['single_entry'] == new_model


def test_home_view_list_title(new_model):
    """Test home view dictionary title attribute."""
    test_request = DummyRequest()
    dic = home_view(test_request)
    assert dic['entry_list'].all()[0].title == 'jill'


def test_home_view_list_text(new_model):
    """Test home view dictionary text attribute."""
    test_request = DummyRequest()
    dic = home_view(test_request)
    assert dic['entry_list'].all()[0].text == 'jello'


def test_home_view_sort_item2_title(new_model):
    """Test home view sort functionality via attribute."""
    new_model = Entry(title="two", text='twotext')
    DBSession.add(new_model)
    DBSession.flush()
    test_request = DummyRequest()
    dic = home_view(test_request)
    assert dic['entry_list'].all()[1].title == 'jill'


def test_home_view_sort_item2_text(new_model):
    """Test home view sort functionality via attribute."""
    new_model = Entry(title="two", text='twotext')
    DBSession.add(new_model)
    DBSession.flush()
    test_request = DummyRequest()
    dic = home_view(test_request)
    assert dic['entry_list'].all()[1].text == 'jello'


def test_home_route(dbtransaction, app):
    """Test home route status code."""
    response = app.get('/')
    assert response.status_code == 200


def test_new_route(dbtransaction, app):
    """Test new route status code."""
    response = app.get('/new')
    assert response.status_code == 200


def test_new_post(dbtransaction, app):
    """Test that a new post is created."""
    db_rows = DBSession.query(Entry).filter(
        Entry.title == 'Testing' and Entry.text == 'Testing')
    assert db_rows.count() == 0
    params = {
        'title': 'Testing',
        'text': 'Testing'
    }
    app.post('/new', params=params, status='3*')
    db_rows = DBSession.query(Entry).filter(
        Entry.title == 'Testing' and Entry.text == 'Testing')
    assert db_rows.count() == 1


def test_new_post_minimum_title_length(dbtransaction, app):
    """Test a new post can't be created without min characters in title."""
    db_rows = DBSession.query(Entry).filter(
        Entry.title == 'a' and Entry.text == 'Testing')
    assert db_rows.count() == 0
    params = {
        'title': 'a',
        'text': 'Testing'
    }
    with pytest.raises(AppError):
        app.post('/new', params=params, status='3*')


def test_new_post_minimum_text_length(dbtransaction, app):
    """Test a new post can't be created without min characters in text."""
    db_rows = DBSession.query(Entry).filter(
        Entry.title == 'Testing2' and Entry.text == 'Test')
    assert db_rows.count() == 0
    params = {
        'title': 'Testing2',
        'text': 'Test'
    }
    with pytest.raises(AppError):
        app.post('/new', params=params, status='3*')


def test_new_post_over_max_title_length(dbtransaction, app):
    """Test that a new post adheres to max title length."""
    mock_title = []
    for i in range(130):
        mock_title.append('a')
    mock_title = "".join(mock_title)
    db_rows = DBSession.query(Entry).filter(
        Entry.title == mock_title and Entry.text == 'Testing')
    assert db_rows.count() == 0
    params = {
        'title': mock_title,
        'text': 'Testing'
    }
    with pytest.raises(AppError):
        app.post('/new', params=params, status='3*')


def test_edit_entry(dbtransaction, app, new_model):
    """Test that a post can be edited."""
    params = {
        'title': 'T' + new_model.title,
        'text': 'T' + new_model.text
    }
    app.post('/edit/{}'.format(new_model.id), params=params, status='3*')
    db_rows = DBSession.query(Entry).filter(
        Entry.title == 'T' + new_model.title and Entry.text == 'T' + new_model.text)
    assert db_rows.count() == 1


def test_edit_entry_min_title_len(dbtransaction, app, new_model):
    """Test that edited title maintains min length conditions."""
    params = {
        'title': 'T',
        'text': 'Testing'
    }
    with pytest.raises(AppError):
        app.post('/edit/{}'.format(new_model.id), params=params, status='3*')


def test_edit_entry_min_text_len(dbtransaction, app, new_model):
    """Test that edited text maintains min length conditions."""
    params = {
        'title': 'Testing',
        'text': 'T'
    }
    with pytest.raises(AppError):
        app.post('/edit/{}'.format(new_model.id), params=params, status='3*')


def test_edit_route(dbtransaction, app, new_model):
    """Test edit route response status."""
    response = app.get('/edit/{}'.format(new_model.id))
    assert response.status_code == 200


def test_entry_route(dbtransaction, app, new_model):
    """Test entry route response status."""
    response = app.get('/entry/{}'.format(new_model.id))
    assert response.status_code == 200


def test_bad_route(dbtransaction, app):
    """Test bad route requests."""
    with pytest.raises(AppError):
        app.get('/entry/{}'.format('whatever'))


def test_home_view_sort_item1_title(dbtransaction, new_model):
    """Test home view sort functionality via attribute."""
    new_model = Entry(title="two", text='twotext')
    DBSession.add(new_model)
    DBSession.flush()
    test_request = DummyRequest()
    dic = home_view(test_request)
    assert dic['entry_list'].all()[0].title == 'two'


def test_home_view_sort_item1_text(new_model):
    """Test home view sort functionality via attribute."""
    new_model = Entry(title="two", text='twotext')
    DBSession.add(new_model)
    DBSession.flush()
    test_request = DummyRequest()
    dic = home_view(test_request)
    assert dic['entry_list'].all()[0].text == 'twotext'
