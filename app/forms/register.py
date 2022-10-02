from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, EmailField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

from .constants_and_validators import username, password as pwd, \
    name, lastname, patronymic, ResetField


class Register(FlaskForm):
    username = StringField(
        "Логин:",
        render_kw={"placeholder": "Ivanious"},
        validators=[
            DataRequired(),
            Length(username.min_length, username.max_length)
        ]
    )
    password = PasswordField(
        "Пароль:",
        validators=[
            DataRequired(),
            Length(pwd.min_length, pwd.max_length,
                   f"Пароль должен быть от {pwd.min_length} до {pwd.max_length} Символов"),
            pwd.validator
        ], render_kw={"placeholder": "********"}
    )
    repeat_password = PasswordField(
        "Повторите пароль:",
        validators=[
            DataRequired(),
            EqualTo("password", "Пароли не совпадают")
        ], render_kw={"placeholder": "********"}
    )
    lastname = StringField(
        "Фамилия:",
        render_kw={"placeholder": "Иванов"},
        validators=[
            DataRequired(),
            Length(lastname.min_length, lastname.max_length),
            lastname.validator
        ]
    )
    name = StringField(
        "Имя:",
        render_kw={"placeholder": "Иван"},
        validators=[
            DataRequired(),
            Length(name.min_length, name.max_length),
            name.validator
        ]
    )
    patronymic = StringField(
        "Отчество:",
        render_kw={"placeholder": "Иванович"},
        validators=[
            DataRequired(),
            Length(patronymic.min_length, patronymic.max_length),
            patronymic.validator
        ]
    )
    email = EmailField(
        "Email:",
        render_kw={"placeholder": "E@mail.ru"},
        validators=[
            DataRequired(),
            Email()
        ]
    )
    sex = RadioField(
        "Пол:",
        choices=[
            (0, "Мужской"),
            (1, "Женский")
        ], default=0
    )
    submit = SubmitField("Отправить")
    reset = ResetField("Сброс")
