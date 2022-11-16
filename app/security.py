from flask_security import SQLAlchemyUserDatastore, Security

from app import app
from app.database import db
from app.models.student import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.before_first_request
def create_user():
    user_datastore.create_user(email='matt@nobien.net', password='password')
    db.session.commit()
