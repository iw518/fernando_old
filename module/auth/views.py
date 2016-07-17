# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        auth views
# Purpose:     auth
#
# Author:      Robot of Fernando
#
# Created:     12-07-2016
# Copyright:   (c) Robot of Fernando 2015
# Licence:     The MIT License
# -------------------------------------------------------------------------------

from flask import render_template

from . import auth


@auth.route('/login')
def login():
    return render_template('auth/login.html')
