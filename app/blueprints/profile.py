import os
from time import mktime

from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from sqlalchemy import func
from werkzeug.utils import secure_filename
from app.models.card_views import CardView
from app.models.users import User
from app.models import db_session
from app.forms.translate_form import TranslateForm

from app.static.CONSTANTS import *

import datetime
from flask import make_response, session

profile_bp = Blueprint('profile', __name__, template_folder='../templates', static_folder='../static')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@profile_bp.route("/upload_avatar", methods=["POST"])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        return jsonify({'success': False, 'error': 'Ключ "avatar" отсутствует в request.files'}), 400

    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Файл не выбран'}), 400

    if file:
        ext = os.path.splitext(file.filename)[1]
        filename = secure_filename(f"user_{current_user.id}{ext}")

        avatar_dir = os.path.join(current_app.root_path, 'static', 'avatars')
        if not os.path.exists(avatar_dir):
            os.makedirs(avatar_dir, exist_ok=True)

        upload_path = os.path.join(avatar_dir, filename)

        # ГАРАНТИРОВАННАЯ ИНИЦИАЛИЗАЦИЯ: объявляем переменную ДО блока сохранения и работы с БД
        db_avatar_path = f"static/avatars/{filename}"

        try:
            # 1. Сохраняем физический файл на диск
            file.save(upload_path)

            # 2. Запись пути в базу данных SQLite
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            user.avatar = db_avatar_path
            db_sess.commit()
            db_sess.close()  # Закрываем сессию, чтобы избежать database is locked

            # 3. Обновляем объект текущего пользователя в текущей сессии Flask-Login
            current_user.avatar = db_avatar_path

            # Возвращаем путь со слэшем для мгновенного отображения во фронтенде
            return jsonify({'success': True, 'path': f"/{db_avatar_path}"})

        except Exception as e:
            # Безопасное закрытие сессии в случае непредвиденного сбоя при записи
            if 'db_sess' in locals():
                db_sess.close()
            return jsonify({'success': False, 'error': f"Системная ошибка: {str(e)}"}), 500

    return jsonify({'success': False, 'error': 'Неподдерживаемый формат файла'}), 400


import datetime
from flask import make_response, request, render_template
from flask_login import login_required, current_user
from app.models import db_session
from app.models.users import User
from app.models.card_views import CardView
from sqlalchemy import func


@profile_bp.route("/user")
@login_required
def user():
    # 1. Расчет статистики дней подряд через Cookies
    today = datetime.date.today()
    last_visit_str = request.cookies.get(f"last_visit_{current_user.id}")
    streak = int(request.cookies.get(f"streak_{current_user.id}", 0))

    if last_visit_str:
        try:
            last_visit = datetime.datetime.strptime(last_visit_str, "%Y-%m-%d").date()
            if last_visit == today - datetime.timedelta(days=1):
                streak += 1
            elif last_visit != today:
                streak = 1
        except ValueError:
            streak = 1
    else:
        streak = 1

    # Использование контекстного менеджера гарантирует автоматическое закрытие сессии SQLite
    with db_session.create_session() as db_sess:
        try:
            # 2. Подсчет общего количества просмотров карточек
            cards_count = db_sess.query(CardView).filter(CardView.user_id == current_user.id).count()

            # 3. Сбор статистики для календаря активности (Генерация матрицы)
            view_data = db_sess.query(
                func.date(CardView.viewed_at).label('date'),
                func.count(CardView.id).label('count')
            ).filter(CardView.user_id == current_user.id).group_by(func.date(CardView.viewed_at)).all()

            activity_dict = {row.date: row.count for row in view_data}

            # Формируем сетку за последние 24 недели
            end_date = today
            start_date = end_date - datetime.timedelta(weeks=24)
            start_date -= datetime.timedelta(days=start_date.weekday())  # Выравниваем на понедельник

            weeks_grid = [[] for _ in range(7)]  # Матрица: 7 дней недели

            current_day = start_date
            while current_day <= end_date:
                date_str = current_day.strftime("%Y-%m-%d")
                count = activity_dict.get(date_str, 0)

                # Присваиваем CSS-класс интенсивности
                if count == 0:
                    color_class = "contrib-color-0"
                elif count <= 2:
                    color_class = "contrib-color-1"
                elif count <= 5:
                    color_class = "contrib-color-2"
                elif count <= 10:
                    color_class = "contrib-color-3"
                else:
                    color_class = "contrib-color-4"

                day_data = {
                    'date': current_day.strftime("%d.%m.%Y"),
                    'count': count,
                    'class': color_class
                }

                weeks_grid[current_day.weekday()].append(day_data)
                current_day += datetime.timedelta(days=1)

            # Извлекаем имя и email пользователя до закрытия сессии
            user_obj = db_sess.query(User).filter(User.id == current_user.id).first()
            user_name = user_obj.name
            user_email = user_obj.email

        except Exception as e:
            db_sess.rollback()
            raise e

    # Формируем HTTP-ответ
    response = make_response(render_template(
        "user.html",
        name=user_name,
        email=user_email,
        streak_days=streak,
        cards_viewed=cards_count,
        weeks_grid=weeks_grid  # Передаем исправленную сетку в шаблон
    ))

    # Сохраняем куки активности на 1 год
    max_age = 60 * 60 * 24 * 365
    response.set_cookie(f"last_visit_{current_user.id}", str(today), max_age=max_age)
    response.set_cookie(f"streak_{current_user.id}", str(streak), max_age=max_age)

    return response
