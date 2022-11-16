from app.database import db


class Doc(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128))
    is_automatic = db.Column(db.Boolean())
    fields = db.Column(db.PickleType())
