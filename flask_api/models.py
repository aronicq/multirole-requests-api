import datetime
import pytz
from db import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, backref


class FunctionsRoles(Base):
    __tablename__ = 'functions_roles_table'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Roles(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    # allowed_methods = Column(String)

    users = relationship('Users', secondary='users_roles', backref=backref('role'))


users_to_roles = Table('users_roles', Base.metadata,
                       Column('user_id', Integer, ForeignKey('users.id')),
                       Column('role_id', Integer, ForeignKey('roles.id'))
                       )


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    @property
    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                }


class Queries(Base):
    __tablename__ = 'queries'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    state = Column(Integer)
    created = Column(Date, default=datetime.datetime.now(tz=pytz.timezone('Europe/Moscow')))
    author = Column(String)

    @property
    def serialize(self):
        return {'id': self.id,
                'text': self.text,
                'state': self.state,
                'created': self.created,
                'author': self.author}

    def __repr__(self):
        return 'text: {}, state: {}, date: {}'.format(self.text, self.state, self.created)
