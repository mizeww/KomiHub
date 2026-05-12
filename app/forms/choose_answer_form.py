from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired


class QuizForm(FlaskForm):
    answer = RadioField('Выберите правильный перевод', validators=[DataRequired()])
    submit = SubmitField('Ответить')


class TrueFalseForm(FlaskForm):
    # Choices: '1' для "Верно", '0' для "Неверно"
    answer = RadioField('Это правильный перевод?',
                        choices=[('1', 'Верно'), ('0', 'Неверно')],
                        validators=[DataRequired()])
    submit = SubmitField('Далее')
