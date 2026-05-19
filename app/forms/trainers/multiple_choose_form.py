from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

class ChoiceTrainerForm(FlaskForm):
    # Варианты ответов (choices) будут подгружаться динамически в роуте
    answer = RadioField('Выберите правильный перевод', validators=[DataRequired()])
    submit = SubmitField('Ответить')