# !/usr/bin/env python
# coding: utf-8

from werkzeug.utils import escape
from wtforms import Field
from wtforms.widgets import HTMLString, html_params


class ButtonWidget(object):
    '''
    用于显示按钮(button)的部件(widget)
    '''
    def __call__(self, field, **kwargs):
        kwargs.setdefault('name', field.name)
        kwargs.setdefault('value', field.value)
        kwargs.setdefault('type', "submit")
        return HTMLString('<button %s>%s</button>' % (
            html_params(**kwargs),
            escape(field._value())
            ))


class ButtonField(Field):
    '''
    定义可以将按钮(button)用于 Flask 表单(form)的域(field)
    '''
    widget = ButtonWidget()

    def __init__(self, text, name='submit', **kwargs):
        super(ButtonField, self).__init__(**kwargs)
        self.text = text
        self.value = text
        self.name = name

    def _value(self):
        return str(self.text)