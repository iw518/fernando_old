#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      __init__
# date:         2016-07-19
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------
from flask import Blueprint
auth = Blueprint('auth',__name__)
from . import views
