import datetime
import sqlalchemy
from app.models.db_session import SqlAlchemyBase

class CardView(SqlAlchemyBase):
    __tablename__ = 'card_views'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    folder = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # 'nouns', 'verbs' и т.д.
    card_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    viewed_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    # Уникальный индекс, чтобы один пользователь не создавал дубли при повторном клике
    __table_args__ = (
        sqlalchemy.UniqueConstraint('user_id', 'folder', 'card_id', name='_user_card_uc'),
    )
