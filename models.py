from flask.ext.login import UserMixin
from flask.ext.sqlalchemy import SQLAlchemy

from .index import app

db=SQLAlchemy(app)
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Interger, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Interger, db.ForeignKey('roles.id'))
