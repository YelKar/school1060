from flask import request

from app.database import db
from app.models.student import User, Info, Role

from passlib.hash import pbkdf2_sha256 as cipher


def add_user(
        username: str, password: str,
        name: str, lastname: str, patronymic: str,
        email: str, sex: bool
):
    sess = db.session
    user = User(
        username=username,
        email=email,
        password=cipher.hash(password),
        current_login_ip=request.remote_addr
    )
    sess.add(user)
    sess.flush()

    info = Info(
        user_id=user.id,
        name=name,
        lastname=lastname,
        patronymic=patronymic,
        sex=int(sex)
    )
    sess.add(info)
    sess.commit()


def assign_role(user_id, role_code, description=None):
    sess = db.session
    role = Role(
        code=role_code,
        description=description
    )
    user = User.query.filter_by(id=user_id).first()
    user.role.append(role)
    sess.add(role)
    sess.commit()
