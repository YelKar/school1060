from datetime import datetime, date

from app.constants import class_letters
from app.database import db


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
    classroom = db.Column(db.Integer())
    admission_year = db.Column(db.Integer())
    classroom_letter = db.Column(db.Integer())
    birthdate = db.Column(db.Integer())

    case = db.relationship("Cases", backref="student", lazy="dynamic")
    father = db.relationship("Father", backref="student", lazy="dynamic")
    mother = db.relationship("Mother", backref="student", lazy="dynamic")
    info = db.relationship("Info", backref="student", lazy="dynamic")

    def __init__(
            self,
            lastname: str = None,
            name: str = None,
            patronymic: str = None,
            **kwargs
    ):
        self.lastname = lastname
        self.name = name
        self.patronymic = patronymic
        super(Students, self).__init__(**kwargs)
        self.grade()

    def fullname(self):
        result = []
        if self.lastname:
            result.append(self.lastname)
        if self.name:
            result.append(self.name)
        if self.patronymic:
            result.append(self.patronymic)
        return " ".join(result)

    def birthdate_to_date(self):
        return date.fromtimestamp(self.birthdate)

    def age(self):
        today = date.today()
        birth = date.fromtimestamp(self.birthdate)
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

    def grade(self) -> int or None:
        now = datetime.now()
        if self.admission_year is None:
            return None
        current_year = now.year
        current_month = now.month
        current_grade = current_year - self.admission_year
        if current_month >= 9:
            current_grade += 1
        if self.classroom != current_grade:
            self.classroom = current_grade
        return current_grade

    def full_grade(self):
        return str(self.grade()) + class_letters[self.classroom_letter]

    def __repr__(self):
        return "<Student{id} => (" \
               "{lastname} {name}{patr}" \
               ")>".format(id=self.id if self.id is not None else "",
                           lastname=self.lastname,
                           name=self.name,
                           patr=(" " + self.patronymic) if self.patronymic else "", )


class Info(db.Model):
    __tablename__ = "student_info"
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey("students.id"), nullable=False)

    phone = db.Column(db.String(32))
    email = db.Column(db.String(256))
    birth_certificate = db.Column(db.String(32))

    home_phone = db.Column(db.String(32))
    address = db.Column(db.String(256))
    parent_emails = db.Column(db.PickleType())


class Father(db.Model):
    __tablename__ = "father"
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(32))
    lastname = db.Column(db.String(64))
    patronymic = db.Column(db.String(64))

    phone = db.Column(db.String(32))

    student_id = db.Column(db.Integer(), db.ForeignKey("students.id"), nullable=False)

    def fullname(self):
        result = []
        if self.lastname:
            result.append(self.lastname)
        if self.name:
            result.append(self.name)
        if self.patronymic:
            result.append(self.patronymic)
        return " ".join(result)


class Mother(db.Model):
    __tablename__ = "mother"
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(32))
    lastname = db.Column(db.String(64))
    patronymic = db.Column(db.String(64))

    phone = db.Column(db.String(32))

    student_id = db.Column(db.Integer(), db.ForeignKey("students.id"), nullable=False)

    def fullname(self):
        result = []
        if self.lastname:
            result.append(self.lastname)
        if self.name:
            result.append(self.name)
        if self.patronymic:
            result.append(self.patronymic)
        return " ".join(result)


class Cases(db.Model):
    from app.models.cases import Case as __Case
    __tablename__ = "cases"
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey("students.id"), nullable=False)

    nomn = db.Column(db.PickleType())
    gent = db.Column(db.PickleType())
    datv = db.Column(db.PickleType())
    accs = db.Column(db.PickleType())
    ablt = db.Column(db.PickleType())
    loct = db.Column(db.PickleType())

    __cases = [
        "gent",
        "datv",
        "accs",
        "ablt",
        "loct",
    ]

    def change(self):
        changed = {"lastname": self.student.lastname,
                   "name": self.student.name,
                   "patronymic": self.student.patronymic}
        self.nomn = changed
        student = self.__Case(self.student.lastname,
                              self.student.name,
                              self.student.patronymic)
        if not student.can_vary():
            return False
        for case in self.__cases:
            changed = student(case)
            changed = {"lastname": changed[0],
                       "name": changed[1],
                       "patronymic": changed[2]}
            exec(f"self.{case} = changed")
        return True
