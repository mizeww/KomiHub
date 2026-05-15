from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from app.models import db_session
from app.models.urls_index import UrlIndex
from app.forms.translate_form import TranslateForm

about_bp = Blueprint('about', __name__, template_folder='../templates', static_folder='../static')

@about_bp.route('/')
def main():
    return render_template("about.html",
                           title='Komi Hub')
