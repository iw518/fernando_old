#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      views
# date:         2016-07-19
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------
import os
import  random
from flask import render_template, redirect,request, url_for, flash
from flask_login import login_user, logout_user, login_required

from app import db
from config import basedir
from . import auth
from .forms import LoginForm, RegisterForm
from ..main.maingui import importMotto
from ..models import User


@auth.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    filename=os.path.join(basedir,'app','config','mottos.xml')
    mottos=importMotto(filename)
    motto=mottos[random.randint(0,len(mottos)-1)]
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verifypassword(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('无效的用户名或密码')
    return render_template('auth/login.html', form=form, motto=motto)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出系统')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['POST','GET'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,fullname=form.fullname.data,password=form.password.data)
        db.session.add(user)
        flash('You have login')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)
