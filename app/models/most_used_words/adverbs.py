import datetime
import sqlalchemy
from sqlalchemy import orm
from app.models.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Adverb(SqlAlchemyBase):

    __tablename__ = 'adverb'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    value = sqlalchemy.Column(sqlalchemy.String)
    translate = sqlalchemy.Column(sqlalchemy.String)

