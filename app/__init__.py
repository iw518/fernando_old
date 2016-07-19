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
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .models import creat_database
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()

    # attach routes and custom error pages here
    from .main import main as main_blueprint
    from .module.analysis import analysis
    from .module.auth import auth as auth_blueprint
    from .module.auth.forms import LoginForm
    from .module.calculation import calculation
    from .module.diagram import diagram
    from .module.fieldWork import fieldWork
    from .module.logginData import logginData
    from .module.statistics import statistics

    app.register_blueprint(main_blueprint)
    app.register_blueprint(logginData, url_prefix="/logginData")
    app.register_blueprint(calculation, url_prefix="/calculation")
    app.register_blueprint(diagram, url_prefix="/logginData")
    app.register_blueprint(statistics, url_prefix="/statistics")
    app.register_blueprint(analysis, url_prefix="/analysis")
    app.register_blueprint(fieldWork, url_prefix="/fieldWork")
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
