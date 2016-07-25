#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      forms
# date:         2016-07-24
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------
from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length

from app.models import User
from app.module.button import ButtonField


class RegisterForm(Form):
    projectIdentifier= StringField('项目编号', validators=[
        DataRequired('请输入项目编号'),
        Length(min=4, max=25, message='length must between 4 and 25')
    ])
    projectName= StringField('项目名称', validators=[
        DataRequired('请输入项目名称'),
        Length(min=4, max=25, message='length must between 4 and 25')
    ])
    submit = ButtonField('确定')


class EmployeeForm(Form):
    projectIdentifier= StringField('项目编号', validators=[
        DataRequired('请输入项目编号'),
        Length(min=4, max=25, message='length must between 4 and 25')
    ])
    projectAssistant= SelectField('项目助理',coerce=int)
    projectManager= SelectField('项目经理',coerce=int)
    testManager= SelectField('土工负责人',coerce=int)
    testAuditor=SelectField('土工审核人',coerce=int)
    projectAuditor=SelectField('项目审核人',coerce=int)
    authorizingPerson= SelectField('项目审定人',coerce=int)
    submit = ButtonField('确定')

    def __init__(self,*args, **kwargs):
        super(EmployeeForm,self).__init__(*args, **kwargs)
        self.projectAssistant.choices=[(user.id,user.username) for user in User.query.all()]
        self.projectManager.choices = [(user.id, user.username) for user in User.query.all()]
        self.testManager.choices = [(user.id, user.username) for user in User.query.all()]
        self.testAuditor.choices = [(user.id, user.username) for user in User.query.all()]
        self.projectAuditor.choices = [(user.id, user.username) for user in User.query.all()]
        self.authorizingPerson.choices = [(user.id, user.username) for user in User.query.all()]

