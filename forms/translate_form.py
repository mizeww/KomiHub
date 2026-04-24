from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TranslateForm(FlaskForm):
    # Поле для ввода слова
    word = StringField('Слово', validators=[DataRequired()], render_kw={"placeholder": "Введите слово..."})
    submit = SubmitField('Перевести')