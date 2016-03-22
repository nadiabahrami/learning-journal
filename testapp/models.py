"""Database Entry model defined."""
import datetime
from sqlalchemy import (
    Column,
    Integer,
    UnicodeText,
    Unicode,
    DateTime
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from zope.sqlalchemy import ZopeTransactionExtension
from jinja2 import Markup
import markdown
from pyramid.security import (
    Allow,
    Everyone,
)

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Wiki(PersistentMapping):
    __name__ = None
    __parent__ = None
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:omnioptents', 'ominpotent')]


def render_markdown(content):
    """Render the fancy markdown for code in text box."""
    fancy_box = Markup(markdown.markdown(content))
    return fancy_box


class Entry(Base):
    __tablename__ = 'journal_entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(128), unique=True)
    text = Column(UnicodeText)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def rendered_text(self):
        """Render markdown when needed."""
        return render_markdown(self.text)
