from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired

class AddCardForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    preview = StringField('Описание', validators=[DataRequired()])
    url = StringField('Ссылка на карточку', validators=[DataRequired()])
    img = StringField('Ссылка на изображение', validators=[DataRequired()])

    submit = SubmitField('Сохранить')