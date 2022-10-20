from datetime import datetime

from .constants import class_letters
from .database import db


# class RolesUsers(db.Model):
#     __tablename__ = "roles_users"
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))
#
#
# class Role(db.Model, RoleMixin):
#     def __init__(self, *args, **kwargs):
#         super(Role, self).__init__(*args, **kwargs)
#         self.role = ROLES[self.code]
#     __tablename__ = "role"
#     id = db.Column(db.Integer(), primary_key=True)
#     code = db.Column(db.Integer())
#     description = db.Column(db.String(255))
#
#
# class User(db.Model, UserMixin):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer(), primary_key=True)
#     email = db.Column(db.String(255), unique=True)
#     username = db.Column(db.String(255))
#     password = db.Column(db.String(255))
#     last_login_at = db.Column(db.DateTime())
#     current_login_at = db.Column(db.DateTime())
#     last_login_ip = db.Column(db.String(100))
#     current_login_ip = db.Column(db.String(100))
#     login_count = db.Column(db.Integer())
#     active = db.Column(db.Boolean())
#     confirmed_at = db.Column(db.DateTime())
#     role = db.relationship('Role', secondary='roles_users',
#                            backref=db.backref('users', lazy='dynamic'))
#     info = db.relationship("Info")
#
#     def set_password(self, password):
#         self.password = pbkdf.hash(password)
#
#     def verify_password(self, password):
#         return pbkdf.verify(password, self.password)
#
#
# class Info(db.Model):
#     __tablename__ = "info"
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
#     name = db.Column(db.String(32))
#     lastname = db.Column(db.String(64))
#     patronymic = db.Column(db.String(64))
#     sex = db.Column(db.Boolean())


class Students(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32))
    lastname = db.Column(db.String(64))
    patronymic = db.Column(db.String(64))
    admission_year = db.Column(db.Integer())
    classroom_letter = db.Column(db.Integer())

    def grade(self):
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        current_grade = current_year - self.admission_year
        if current_month < 9:
            current_grade -= 1
        return current_grade

    def full_grade(self):
        return str(self.grade()) + class_letters[self.classroom_letter]
