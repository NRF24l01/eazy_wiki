from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Wiki(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    desc = db.Column(db.String(250))
    path_to_md = db.Column(db.String(75))
    path_to_logo = db.Column(db.String(75))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(10))
    can_read = db.Column(db.Boolean())
    can_write = db.Column(db.Boolean())
