# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        initial auth
# Purpose:     auth
#
# Author:      Robot of Fernando
#
# Created:     12-07-2016
# Copyright:   (c) Robot of Fernando 2015
# Licence:     The MIT License
# -------------------------------------------------------------------------------

from flask import Blueprint


auth = Blueprint('auth', __name__)


from . import views
