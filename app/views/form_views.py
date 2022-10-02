from flask import render_template

from app import app
from app.accounts import add_user
from app.forms.login import Login
from app.forms.register import Register

from colorama import Style, Fore, Back


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = "Регистрация"
    form = Register()
    if form.validate_on_submit():
        print(f"{Fore.LIGHTWHITE_EX}{Back.BLUE}{Style.BRIGHT}"
              f"   {'Имя поля':20} | Данные   "
              f"{Style.RESET_ALL}{Back.BLUE}{Fore.BLACK}")
        for name, data in form.data.items():
            print(f"   {name:20} | {data:50} | {type(data)}   ")  # if 'password' not in name else cipher.hash(data)

        add_user(
            form.username.data,
            form.password.data,
            form.name.data,
            form.lastname.data,
            form.patronymic.data,
            form.email.data,
            form.sex.data,
        )
    return render_template("forms/register.html", form=form, title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Войти"
    form = Login()
    if form.validate_on_submit():
        pass
    return render_template("forms/login.html",
                           form=form,
                           title=title)
