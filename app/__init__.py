#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      __init__.py
# date:         2016-07-19
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager=LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    from .models import User

    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()
        from app.models import Role
        Role.insert_roles()

    # attach routes and custom error pages here
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .module import audit_blueprint, analysis_blueprint,calculation_blueprint,diagram_blueprint,fieldWork_blueprint,logginData_blueprint,order_blueprint,statistics_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(audit_blueprint, url_prefix='/audit')
    app.register_blueprint(logginData_blueprint, url_prefix="/logginData")
    app.register_blueprint(calculation_blueprint, url_prefix="/calculation")
    app.register_blueprint(diagram_blueprint, url_prefix="/logginData")
    app.register_blueprint(statistics_blueprint, url_prefix="/statistics")
    app.register_blueprint(analysis_blueprint, url_prefix="/analysis")
    app.register_blueprint(fieldWork_blueprint, url_prefix="/fieldWork")
    app.register_blueprint(order_blueprint, url_prefix="/order")

    return app
