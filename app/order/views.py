#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      views
# date:         2016-07-24
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------
from flask import render_template, redirect, url_for,flash,request

from app import db
from . import order
from .forms import RegisterForm, EmployeeForm
from ..models import Project, Registration


@order.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        project = Project(identifier=form.projectIdentifier.data, name=form.projectName.data)
        db.session.add(project)
        return redirect(url_for('order.employee'))
    return render_template('order/register.html', form=form)


@order.route('/employee', methods=['POST', 'GET'])
def employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        project_identifier = form.projectIdentifier.data
        employee_dict = {'projectAssistant': 'ProjectAssistant', 'projectManager': 'ProjectManager',
                  'projectAuditor': 'ProjectAuditor', 'authorizingPerson': 'AuthorizingPerson',
                  'testManager': 'TestManager', 'testAuditor': 'TestAuditor'}
        for key in employee_dict:
            form_control = getattr(form, key)
            user_id=form_control.data
            role_name=employee_dict[key]
            registration = Registration(project_identifier=project_identifier, user_id=user_id,
                                        role_name=role_name)
            if Registration.is_exsit(registration) is None:
                db.session.add(registration)
            else:
                flash('不允许一个人身兼多职!')
                return render_template('order/employee.html', form=form)
        db.session.commit()
        project = Project.query.filter_by(identifier=project_identifier).first()
        return render_template('order/profile.html', project=project)
    return render_template('order/employee.html', form=form)

@order.route('/profile')
def profile():
    projectNo=request.args.get('projectNo')
    project = Project.query.filter_by(identifier=projectNo).first()

    return render_template('order/profile.html', project=project)