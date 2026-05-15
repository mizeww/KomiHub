from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Текущий пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[
        DataRequired()
    ])
    confirm_password = PasswordField('Повторите новый пароль', validators=[
        DataRequired(),
        EqualTo('new_password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Обновить пароль')
