import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy import event  # <-- Добавьте этот импорт

SqlAlchemyBase = orm.declarative_base()
__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    # ИСПРАВЛЕНО: Добавляем принудительный таймаут в 30 секунд на уровне движка
    engine = sa.create_engine(conn_str, echo=False, connect_args={'timeout': 30})

    # ИСПРАВЛЕНО: Автоматически переводим SQLite в режим WAL при подключении
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.close()

    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> orm.Session:
    global __factory
    return __factory()
