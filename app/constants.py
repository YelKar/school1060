CONTEXT_CONSTANTS = dict(
    base="bases/base.html",
    form_base="bases/form_base.html",
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
class_letters = {0: "н", 1: "о", 2: "п"}
# Создание постоянных с кодами ролей
for code, name in enumerate(ROLES):
    exec(f"{name}: int = {code}")

# Sex
MALE = 0
FEMALE = 1
