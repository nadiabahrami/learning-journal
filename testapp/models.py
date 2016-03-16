from sqlalchemy import (
    Column,
    String,
    Index,
    Integer,
    Text,
    Time,
    UnicodeText,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Entry(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    title = Column(UnicodeText(128), unique=True)
    text = Column(UnicodeText)
    created = Column(Time)
    
Index('my_index', Entry.title, unique=True, mysql_length=255)
