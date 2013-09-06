# -*- coding: utf-8 -*-

import datetime
import json
import os

from rfc3339 import rfc3339

from sqlalchemy import create_engine, ForeignKey, UniqueConstraint
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()
Error = SQLAlchemyError

options = {"echo": True}
url = 'sqlite:///{0}'.format(
    os.path.join(os.path.dirname(__file__), "database.db")
)

# if 'DOTCLOUD_PROJECT' in os.environ:
#     url = "mysql+mysqldb://{login}:{password}@{host}:{port}/db".format(
#         login=os.environ['DOTCLOUD_DB_MYSQL_LOGIN'],
#         password=os.environ['DOTCLOUD_DB_MYSQL_PASSWORD'],
#         host=os.environ['DOTCLOUD_DB_MYSQL_HOST'],
#         port=os.environ['DOTCLOUD_DB_MYSQL_PORT']
#     )

#     options['pool_recycle'] = 3600
#     options['pool_size'] = 20
#     options['max_overflow'] = 10
#     options['echo'] = False

engine = create_engine(url, **options)
session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine))

Error = SQLAlchemyError

class HelperBase(object):
    def to_dict(self):
        res = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, (datetime.datetime, datetime.date)):
                value = rfc3339(value)
            res[column.name] = value
        return res

    def to_json(self, *args, **kwargs):
        return json.dumps(self.to_dict(), *args, **kwargs)

    def __repr__(self):
        return "<{0}({1})>".format(
            self.__class__.__name__,
            ", ".join([
                "{0}={1}".format(k, v) for k, v in self.to_dict().iteritems()
            ])
        )


class Repository(Base, HelperBase):
    __tablename__ = 'repositories'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False, unique=True)


class Tag(Base, HelperBase):
    __tablename__ = 'tags'
    __table_args__ = (
        UniqueConstraint("name", "repo_id"),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    repo_id = Column(Integer, ForeignKey("repositories.id"))
