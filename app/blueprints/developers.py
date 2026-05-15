from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from app.models import db_session
from app.models.urls_index import UrlIndex
from app.forms.translate_form import TranslateForm

developers_bp = Blueprint('developers_bp', __name__, template_folder='../templates', static_folder='../static')

@developers_bp.route('/')
def main():
    return render_template("developers.html",
                           title='Komi Hub')
