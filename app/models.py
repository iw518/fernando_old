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


class Permission:
    View_ENTRY = 0x01
    SITE_ENTRY = 0x02
    DATA_ENTRY = 0x04
    TEST_ENTRY = 0x08
    OPINION_ENTRY = 0x10
    AUTHORIZED = 0x20
    USER_ENTRY = 0x40

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    identifier = db.Column(db.String(64), unique=True)
    opinions = db.relationship('Opinion', backref='project')
    users = db.relationship('User', secondary='registrations', backref=db.backref('projects', lazy='select'),
                            lazy='select')
    registrations=db.relationship('Registration')
    profile = db.relationship('Profile',uselist=False)

    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier


class Registration(db.Model):
    __tablename__ = 'registrations'
    # 复合主键
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, project_identifier, user_id, role_name):
        project = Project.query.filter_by(identifier=project_identifier).first()
        role = Role.query.filter_by(name=role_name).first()
        self.project_id = project.id
        self.user_id = user_id
        self.role_id = role.id

    @classmethod
    def is_exsit(cls,registration):
        if cls.query.filter_by(project_id=registration.project_id).first():
            return cls.query.filter_by(user_id=registration.user_id).first()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    fullname = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    registrations = db.relationship('Registration',backref='user')

    def __init__(self, username, fullname, email, password):
        self.username = username
        self.fullname = fullname
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verifypassword(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Integer)
    fullname = db.Column(db.String(64))
    users = db.relationship('Registration', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'Guest': (Permission.View_ENTRY, True,'来宾'),
            'TestManager': (Permission.TEST_ENTRY, False,'试验负责人'),
            'TestAuditor': (Permission.TEST_ENTRY | Permission.View_ENTRY, False,'试验审核人'),
            'Worker': (Permission.SITE_ENTRY, False,'作业人员'),
            'ProjectAssistant': (Permission.DATA_ENTRY | Permission.SITE_ENTRY | Permission.View_ENTRY, False,'项目助理'),
            'ProjectManager': (
            Permission.DATA_ENTRY | Permission.TEST_ENTRY | Permission.SITE_ENTRY | Permission.View_ENTRY, False,'项目经理'),
            'ProjectAuditor': (Permission.OPINION_ENTRY | Permission.View_ENTRY, False,'项目审核人'),
            'AuthorizingPerson': (Permission.AUTHORIZED | Permission.OPINION_ENTRY | Permission.View_ENTRY, False,'项目审定人'),
            'UserManager': (Permission.USER_ENTRY, False,'用户管理员'),
            'Administrator': (0xff, False,'管理员')
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            role.fullname = roles[r][2]
            db.session.add(role)
        db.session.commit()


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    phase = db.Column(db.String(8))
    client = db.Column(db.String(32))
    design = db.Column(db.String(32))
    size=db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, phase, client, design):
        self.phase = phase
        self.client = client
        self.design = design


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    profiles = db.relationship('Profile', backref='category')

    def __init__(self, name):
        self.name = name


class Opinion(db.Model):
    __tablename__ = 'opinions'
    id = db.Column(db.Integer, primary_key=True)
    stage = db.Column(db.String(64))
    content = db.Column(db.Text())
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, project_id,stage, content):
        self.project_id=project_id
        self.stage = stage
        self.content = content


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
