# -*- coding: utf-8 -*-
from testapp.models import Entry, DBSession, render_markdown


def test_create_entry(dbtransaction):
    """Test for a change of state of the model."""
    new_model = Entry(title="jill", text='jello')
    assert new_model.id is None
    DBSession.add(new_model)
    DBSession.flush()
    assert new_model.id is not None


def test_render_markdown():
    """Assert render markdown works."""
    content = 'Hello'
    output = render_markdown(content)
    assert output == '<p>Hello</p>'
