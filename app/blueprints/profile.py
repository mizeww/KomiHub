import os

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.models.users import User
from app.models import db_session
from app.forms.translate_form import TranslateForm

from app.static.CONSTANTS import *

profile_bp = Blueprint('profile', __name__, template_folder='../templates', static_folder='../static')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@profile_bp.route('/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        return jsonify({'success': False, 'error': 'Нет файла'})

    file = request.files['avatar']

    if file.filename == '':
        return jsonify({'success': False, 'error': 'Файл не выбран'})

    if file and allowed_file(file.filename):
        filename = secure_filename(f"user_{current_user.id}_{file.filename}")
        filepath = os.path.join(profile_bp.config['UPLOAD_FOLDER'], filename)

        file.save(filepath)

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.avatar = f'/static/avatars/{filename}'
        db_sess.commit()

        return jsonify({
            'success': True,
            'avatar_url': user.avatar,
            'message': 'Изображение успешно загружено'
        })

    return jsonify({'success': False, 'error': 'Неверный формат файла'})


@profile_bp.route("/user")
@login_required
def user():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    return render_template("user.html", name=user.name, email=user.email, TranslateForm=TranslateForm())
