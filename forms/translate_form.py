from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    text = TextAreaField('Введите текст')
    submit = SubmitField('Отправить')