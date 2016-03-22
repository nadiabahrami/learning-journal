from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from .models import (
    DBSession,
    Entry,
)
from pyramid.httpexceptions import HTTPFound
from jinja2 import Markup
import markdown
from testapp.formclass import EntryForm
from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    )


from .security import USERS


@view_config(route_name='new', renderer='templates/add.jinja2', permission='omnipotent')
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


@view_config(route_name='edit', renderer='templates/add.jinja2', permission='omnipotent')
def edit_entry(request):
    """Create a form page for an edited entry."""
    edit_id = request.matchdict['id']
    edit_entry = DBSession.query(Entry).get(edit_id)
    # edit_entry.text = render_markdown(edit_entry.text) #trying to get edited entyr to not show html
    form = EntryForm(request.POST, edit_entry)
    if request.method == "POST" and form.validate():
        # edit_entry.text = Markup(edit_entry.text)
        # edit_entry.text = render_markdown(edit_entry.text)
        # # edit_entry.text = Markup.striptags(edit_entry.text) #trying to get edited entyr to not show html
        form.populate_obj(edit_entry)
        DBSession.add(edit_entry)
        DBSession.flush()
        url = request.route_url('entry', id=edit_entry.id)
        return HTTPFound(location=url)
    return {'form': form}


@view_config(route_name='home', renderer='templates/list.jinja2')
def home_view(request):
    """Render home page with database list."""
    print(request)
    try:
        entry_list = DBSession.query(Entry).order_by(Entry.id.desc(), permission='viewer')
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'entry_list': entry_list}


@view_config(route_name='entry', renderer='templates/detail.jinja2', permission='omnipotent')
def entry_view(request):
    """Render a single page detailed view of an entry."""
    try:
        entry_id = request.matchdict['id']
        single_entry = DBSession.query(Entry).filter(Entry.id == entry_id).first()
        # single_entry.text = render_markdown(single_entry.text)
    except DBAPIError:  # Can't figure out how to test this. :(
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'single_entry': single_entry}


@view_config(context='.models.Wiki', name='login',
             renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    login_url = request.resource_url(request.context, 'login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if USERS.get(login) == password:
            headers = remember(request, login)
            return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Failed login'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        )

@view_config(context='.models.Wiki', name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.resource_url(request.context),
                     headers = headers)

# def render_markdown(content):
#     """Render the fancy markdown for code in text box."""
#     fancy_box = Markup(markdown.markdown(content))
#     return fancy_box


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_testapp_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
