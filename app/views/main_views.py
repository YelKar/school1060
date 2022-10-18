# from .form_views import *

from app import app

e = (i for i in range(1000))


@app.route("/")
def index():
    title = "School1060"
    return render_template("index.html", title=title)


from .docs_views import *
# @app.route('/test')
# def test():
#     user = User(
#         email=f"karamyshev_e{next(e)}@1060.ru",
#         username="YelKar",
#         password="12345678",
#     )
#     db.session.add(user)
#     db.session.flush()
#     info = Info(
#         name="Елисей",
#         lastname="Карамышев",
#         patronymic="Александрович",
#         sex=True,
#         user_id=user.id
#     )
#     role = Role(
#         name="Студент"
#     )
#     db.session.add(role)
#     db.session.add(info)
#     db.session.flush()
#     role_user = RolesUsers(
#         user_id=user.id,
#         role_id=role.id
#     )
#     db.session.add(role_user)
#     db.session.commit()
#     return "test"
