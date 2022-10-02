from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from app.forms.constants_and_validators import ResetField, login_validator


class Login(FlaskForm):
    login = StringField(
        "Логин:",
        render_kw={"placeholder": "Введите email или логин"},
        validators=[
            DataRequired(),
            login_validator
        ]
    )
    password = PasswordField(
        "Пароль:",
        render_kw={"placeholder": "******"},
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField(
        "Отправить"
    )
    reset = ResetField("Сброс")