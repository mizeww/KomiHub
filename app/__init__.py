from datetime import datetime

from flask import Flask
from app.config import DevelopmentConfig
from app.extensions import db, login_manager, csrf
from .models import db_session
from .models.users import User


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)

    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    db_session.global_init('instance/blogs.db')
    db_sess = db_session.create_session()

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        try:
            # Flask-Login вызывает эту функцию при каждом обновлении любой страницы
            return db_sess.query(User).get(int(user_id))
        except Exception:
            return None
        finally:
            db_sess.close()  # ГАРАНТИРОВАННО СНИМАЕМ БЛОКИРОВКУ ПОСЛЕ ПРОВЕРКИ

    # Регистрация Blueprints
    from app.blueprints.main import main_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.profile import profile_bp
    from app.blueprints.cards import cards_bp
    from app.blueprints.cookie import cookie_bp
    from app.blueprints.translate import translate_bp
    from app.blueprints.developers import developers_bp
    from app.blueprints.about import about_bp
    from app.blueprints.trainers import trainers_bp
    # from app.blueprints.lessons import lessons_bp
    from app.blueprints.info import info_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(cards_bp, url_prefix='/cards')
    app.register_blueprint(cookie_bp, url_prefix='/cookies')
    app.register_blueprint(translate_bp)
    app.register_blueprint(developers_bp, url_prefix='/developers')
    app.register_blueprint(about_bp, url_prefix='/about')
    app.register_blueprint(trainers_bp, url_prefix='/trainers')
    # app.register_blueprint(lessons_bp, url_prefix='/lessons')
    app.register_blueprint(info_bp)

    @app.context_processor
    def inject_common_variables():
        from app.forms.translate_form import TranslateForm

        return {'TranslateForm': TranslateForm(),
                'current_year': datetime.now().year,
                'debug': app.debug}


    # Создание папки instance, если её нет
    with app.app_context():
        import os
        os.makedirs('instance', exist_ok=True)

    return app
