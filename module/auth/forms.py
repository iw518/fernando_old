from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, InputRequired

from .button import ButtonField


class LoginForm(Form):
    userID = StringField('userID',validators=[
        DataRequired('Please enter IDs'),
        Length(min = 4, max = 25, message='length must between 4 and 25')
    ])
    password = PasswordField('PassWord', validators=[
        InputRequired('Please enter password'),
        Length(min = 6, max = 16, message='length must between 4 and 25')
    ])
    submit = ButtonField('登陆','Submit')