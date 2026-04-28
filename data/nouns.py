import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Noun(SqlAlchemyBase):

    __tablename__ = 'noun'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    value = sqlalchemy.Column(sqlalchemy.String)
    translate = sqlalchemy.Column(sqlalchemy.String)

