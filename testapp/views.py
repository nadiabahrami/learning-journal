"""Create view paths with authentication variables."""
from pyramid.view import view_config
from .models import (
    DBSession,
    Entry,
)
from pyramid.httpexceptions import HTTPFound
from testapp.formclass import EntryForm
from pyramid.security import (
    remember,
    forget,
)
from testapp.security import check_pw


@view_config(route_name='new',  # check_csrf=True,  # CSRF
             renderer='templates/add.jinja2', permission='omnipotent')
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


@view_config(route_name='edit',  # check_csrf=True,  # CSRF
             renderer='templates/add.jinja2', permission='omnipotent')
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


@view_config(route_name='home',  # check_csrf=True,  # CSRF
             renderer='templates/list.jinja2', permission='viewer')
def home_view(request):
    """Render home page with database clickable list."""
    entry_list = DBSession.query(Entry).order_by(Entry.id.desc())
    return {'entry_list': entry_list}


@view_config(route_name='entry',  # check_csrf=True,  # CSRF
             renderer='templates/detail.jinja2', permission='viewer')
def entry_view(request):
    """Render a single page detailed view of an entry."""
    entry_id = request.matchdict['id']
    single_entry = DBSession.query(Entry).filter(Entry.id == entry_id).first()
    return {'single_entry': single_entry}


@view_config(route_name='login', context=".models.MyRoot",
             renderer='templates/login.jinja2')
def login(request):
    """Render lgin view."""
    if request.method == 'POST':
        username = request.params.get('username', '')
        password = request.params.get('password', '')
        if check_pw(password):
            headers = remember(request, username)
            # token = request.session.new_csrf_token()  # CSRF
            return HTTPFound('/home', headers=headers)
    return {}


@view_config(route_name='logout')
def logout(request):
    """Allow logout functionality."""
    headers = forget(request)
    return HTTPFound(request.route_url('login'), headers=headers)
