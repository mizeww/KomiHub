from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class InputTrainerForm(FlaskForm):
    answer = StringField('Введите перевод слова', validators=[DataRequired()])
    submit = SubmitField('Проверить')