import datetime

import pytz as pytz
from db import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey

class FunctionsRoles(Base):
    __tablename__ = 'functions_roles_table'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class RolesTable(Base):
    __tablename__ = 'user_roles_table'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    role_id = Column(Integer, ForeignKey(RolesTable.id))
    is_user = Column(Boolean)
    is_operator = Column(Boolean)
    is_admin = Column(Boolean)

    @property
    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'is_user': self.is_user,
                'is_operator': self.is_operator,
                'is_admin': self.is_admin}


class Queries(Base):
    __tablename__ = 'queries'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    state = Column(Integer)
    created = Column(Date, default=datetime.datetime.now(tz=pytz.timezone('Europe/Moscow')))

    @property
    def serialize(self):
        return {'id': self.id,
                'text': self.text,
                'state': self.state,
                'created': self.created}

    def __repr__(self):
        return 'text: {}, state: {}, date: {}'.format(self.text, self.state, self.created)
