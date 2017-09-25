from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):

    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')



class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                                   0, 'Usernames must have only letters,'
                                                   'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already in use.')


# 修改密码
class ChangePasswordForm(Form):
    '''  修改密码 '''
    old_password = PasswordField(u'Old Password', validators=[Required()])
    password = PasswordField(u'New Password', validators=[Required(), EqualTo('password2', message=u'您两次输入的新密码不一致')])
    password2 = PasswordField(u'Input Password Again', validators=[Required()])
    submit = SubmitField(u'更新密码')


# 重置密码
class PasswordResetRequestForm(Form):
    '''  重置密码请求 '''
    email = StringField(u'Email', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField(u'Reset Password')


class PasswordResetForm(Form):
    '''  重置密码  '''
    email = StringField(u'Account', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField(u'New Password', validators=[Required(), EqualTo('password2', message=u'您两次输入的新密码不一致')])
    password2 = PasswordField(u'Input Password Again', validators=[Required()])
    submit = SubmitField(u'Reset')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'The email address not exist')


# 修改邮件地址
class ChangeEmailForm(Form):
    '''  修改邮件地址 '''
    email = StringField(u'New Email Address', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField(u'Password', validators=[Required()])
    submit = SubmitField(u'Change')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'This email address has been registered')

