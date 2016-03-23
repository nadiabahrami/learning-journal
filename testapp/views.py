# -*- coding: utf-8 -*-
"""View module that contains all view template hookup functions."""
from pyramid.view import view_config
from .models import (
    DBSession,
    Entry,
)
from pyramid.httpexceptions import HTTPFound
from testapp.formclass import EntryForm


@view_config(route_name='new', renderer='templates/add.jinja2')
def new_entry(request):
    """Create a form page for a new entry."""
    form = EntryForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_entry = Entry(title=form.title.data, text=form.text.data)
        DBSession.add(new_entry)
        DBSession.flush()
        url = request.route_url('entry', id=new_entry.id)
        return HTTPFound(location=url)
    return {'form': form}


@view_config(route_name='edit', renderer='templates/add.jinja2')
def edit_entry(request):
    """Create a form page for an edited entry."""
    edit_id = request.matchdict['id']
    edit_entry = DBSession.query(Entry).get(edit_id)
    form = EntryForm(request.POST, edit_entry)
    if request.method == "POST" and form.validate():
        form.populate_obj(edit_entry)
        DBSession.add(edit_entry)
        DBSession.flush()
        url = request.route_url('entry', id=edit_entry.id)
        return HTTPFound(location=url)
    return {'form': form}


@view_config(route_name='home', renderer='templates/list.jinja2')
def home_view(request):
    """Render home page with database list."""
    entry_list = DBSession.query(Entry).order_by(Entry.id.desc())
    return {'entry_list': entry_list}


@view_config(route_name='entry', renderer='templates/detail.jinja2')
def entry_view(request):
    """Render a single page detailed view of an entry."""
    entry_id = request.matchdict['id']
    single_entry = DBSession.query(Entry).filter(Entry.id == entry_id).first()
    return {'single_entry': single_entry}
