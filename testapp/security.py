

USERS = {'omnipotent':'omnipotent',
          'viewer':'viewer'}
GROUPS = {'omnipotent':['group:omnipotents']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])

config.add_view('testapp.views.new_entry',
                name='add_entry.html',
                context='mypackage.resources.Blog',
                permission='omnipotent')

config.add_view('testapp.views.edit_entry',
                name='add_entry.html',
                context='mypackage.resources.Blog',
                permission='omnipotent')

config.add_view('testapp.views.home_view',
                name='add_entry.html',
                context='mypackage.resources.Blog',
                permission='omnipotent')

config.add_view('testapp.views.entry_view',
                name='add_entry.html',
                context='mypackage.resources.Blog',
                permission='omnipotent')

from pyramid.view import view_config
from resources import Blog

@view_config(context=Blog, name='add_entry.html', permission='add')
def blog_entry_add_view(request):
    """ Add blog entry code goes here """
    pass