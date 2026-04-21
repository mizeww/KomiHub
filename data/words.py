import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Word(SqlAlchemyBase):

    __tablename__ = 'word'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    value = sqlalchemy.Column(sqlalchemy.String)

    suffix = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    translate = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    example = sqlalchemy.Column(sqlalchemy.String, nullable=True)
