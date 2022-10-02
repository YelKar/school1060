from dataclasses import dataclass

from passlib.hash import pbkdf2_sha256 as pbkdf
from wtforms import PasswordField, ValidationError, StringField, SubmitField
from wtforms.widgets import SubmitInput

from app.models import User


class ResetField(SubmitField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = SubmitInput()
        self.widget.input_type = "reset"
        self.type = "ResetField"


@dataclass
class Password:
    min_length = 6
    max_length = 30

    @staticmethod
    def validator(_, field: PasswordField):
        """
        Пароль должен содержать только символы пригодные для печати
        Непечатаемые символы - это те символы,
        которые определены в базе данных символов Юникода как “Другие” или “Разделитель”.
        """
        if not field.data.isprintable():
            raise ValidationError("Пароль содержит недопустимые символы")
        elif field.data.isnumeric():  # Пароль не должен содержать только цифры
            raise ValidationError("Пароль должен содержать буквы")
        elif field.data.isalpha():  # Пароль не должен содержать только буквы
            raise ValidationError("Пароль должен содержать цифры")
        elif field.data.islower():  # Пароль не должен содержать только строчные буквы
            raise ValidationError("Пароль должен содержать заглавные буквы")
        elif field.data.isupper():  # Пароль не должен содержать только заглавные буквы
            raise ValidationError("Пароль должен содержать строчные буквы")


@dataclass
class Username:
    min_length = 3
    max_length = 30


@dataclass
class FullName:
    min_length = 2
    max_length = 30

    @staticmethod
    def validator(_, field: StringField):
        first: str = field.data[0]
        lower_letters: str = field.data[1:]
        if not field.data.isalpha():
            raise ValidationError(f"{field.label[:-1]} должно(-а) состоять только из букв")
        elif not first.isupper():
            raise ValidationError(f"Первая буква должна быть заглавной")
        elif not lower_letters.islower():
            raise ValidationError(f"Все буквы кроме первой должны быть заглавными")


name = lastname = patronymic = FullName()

password = Password()
username = Username()


def login_validator(form, __):
    filt = User.query.filter_by
    user = filt(email=form.login.data.lower()).first() \
        or filt(username=form.login.data).first()
    if user and user.verify_password(form.password.data):
        raise ValidationError("Валидация пройдена")
    raise ValidationError("Неверный логин или пароль")
