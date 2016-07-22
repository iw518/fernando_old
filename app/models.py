#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      models.py
# date:         2016-07-19
# copyright:    copyright  2016 Xu, Aiwu
# --
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from . import login_manager


class User(UserMixin,db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    fullname = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash=db.Column(db.String(128))
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __init__(self, username, fullname,email,password):
        self.username = username
        self.fullname= fullname
        self.email = email
        self.password=password

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verifypassword(self, password):
        return check_password_hash(self.password_hash,password)


class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key=True)
    users=db.relationship('User',backref='role')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

