from datetime import datetime


CONTEXT_CONSTANTS = dict(
    base="bases/base.html",
    students_base="bases/select_students.html",
    about_site="School1060",
)

# Roles
ROLES: list[str] = [
    "ADMIN",
    "DIRECTOR",
    "HEAD_TEACHER",
    "STUDENT"
]
# Class Letters
class_letters = {0: "Н", 1: "О", 2: "П"}
# Создание постоянных с кодами ролей
for code, name in enumerate(ROLES):
    exec(f"{name}: int = {code}")

# Sex
MALE = 0
FEMALE = 1


def year_to_classroom(year):
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    classroom = current_year - year
    if current_month < 9:
        classroom -= 1
    return classroom
