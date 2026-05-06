from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from app.models import db_session
from app.models.urls_index import UrlIndex
from app.forms.translate_form import TranslateForm

main_bp = Blueprint('main', __name__, template_folder='../templates', static_folder='../static')

@main_bp.route('/')
def index():
    db_sess = db_session.create_session()

    items = db_sess.query(UrlIndex).order_by(UrlIndex.id).all()

    return render_template("index.html",
                           title='Komi Hub',
                           items=items)
