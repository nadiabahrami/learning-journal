"""Initialize page and main function."""
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .models import (
    DBSession,
    Base,
)
from testapp.security import groupfinder
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from testapp.models import MyRoot


def main(global_config, **settings):
    """Function returns a Pyramid WSGI application."""
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authn_policy = AuthTktAuthenticationPolicy('secret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(
        settings=settings,
        root_factory=MyRoot
    )
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_route('home', '/home')
    config.add_route('entry', '/entry/{id:\d+}')
    config.add_route('new', '/new')
    config.add_route('edit', '/edit/{id:\d+}')
    config.add_route('login', '/')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
