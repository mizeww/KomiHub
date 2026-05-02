from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired

class ChangeCardForm(FlaskForm):
    name = StringField('Название карточки, которую надо изменить', validators=[DataRequired()])
    new_name = StringField('Новое название', validators=[DataRequired()])
    preview = StringField('Новое описание', validators=[DataRequired()])
    url = StringField('Новая ссылка на карточку', validators=[DataRequired()])
    img = StringField('Новая ссылка на изображение', validators=[DataRequired()])

    submit = SubmitField('Сохранить')