import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgres://postgres:password@db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)

    admin = models.Roles(name='Admin')
    operator = models.Roles(name='Operator')
    user = models.Roles(name='User')

    print(str(db_session.query(models.Roles).all()), file=sys.stderr)
    if not db_session.query(models.Roles).all():
        db_session.add(admin)
        db_session.add(operator)
        db_session.add(user)
        db_session.commit()
        print("roles added", file=sys.stderr)

    ivan = models.Users(name='Ivan')
    maria = models.Users(name='Maria')
    kate = models.Users(name='Kate')
    gleb = models.Users(name='Gleb')

    print(str(db_session.query(models.Users).all()), file=sys.stderr)
    if not db_session.query(models.Users).all():
        db_session.add(ivan)
        db_session.add(maria)
        db_session.add(kate)
        db_session.add(gleb)
        db_session.commit()

    if not db_session.query(models.users_to_roles).all():
        ivan.role.append(user)
        maria.role.append(operator)
        kate.role.append(admin)
        gleb.role.append(operator)
        gleb.role.append(admin)
        db_session.commit()

