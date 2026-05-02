from flask import Blueprint, render_template

from app.models import db_session
from app.forms.translate_form import TranslateForm
from app.models.words import Word

translate_bp = Blueprint('translate', __name__, template_folder='../templates', static_folder='../static')


@translate_bp.route('/translate/<word>')
def translate(word):
    db_sess = db_session.create_session()
    data1 = db_sess.query(Word).filter(Word.value == word.lower()).first()
    data2 = db_sess.query(Word).filter(Word.translate.like(f'%{word.lower()}%')).first()

    res = ''

    if data1:
        strdata = data1.translate
        for i in strdata:
            if i not in "['']":
                res += i
    elif data2:
        strdata = data2.value
        for i in strdata:
            if i not in "['']":
                res += i

    if not res:
        res = 'Слово не найдено'

    return render_template("translate.html",
                           word=word,
                           translate=res,
                           title="Komi Lang",
                           TranslateForm=TranslateForm())
