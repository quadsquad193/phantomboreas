from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Required, Length, EqualTo

class UsernamePasswordForm(Form):
    username = TextField('Username', validators=[
    	Required(message='Username is required')
    ])
    password = PasswordField('Password', validators=[
    	Required(message='Password is required')
    ])

class RegisterForm(Form):
    username = TextField('Username', validators=[
    	Required(message='Username is required'),
    	Length(min=6, max=32, message='Username must be between 6 and 32 characters')
    ])
    password = PasswordField('Password', validators=[
    	Required(message='Password is required'),
    	Length(min=6, max=32, message='Password must be between 6 and 32 characters'),
    	EqualTo('confirm', message="Passwords must match")
    ])
    confirm = PasswordField('Password', validators=[Required(message='Please confirm password')])