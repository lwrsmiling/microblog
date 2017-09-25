#!/usr/bin/python
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import os
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager,Shell
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
Bootstrap(app)
moment = Moment(app)


#set flask-wtf
app.config['SECRET_KEY'] = 'hard to guess string'

#config database
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#config gmail
app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

#config email support
# app.config['FLASKY_MAIL_SUBJECT_PREFIX'] ='[FLASKY]'
# app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <wanru@ualberta.ca>'

# def send_email(to, subject, template, **kwargs):
#     msg = Message('Subject',sender=os.environ.get('MAIL_USERNAME'),recipients=['401462312@qq.com'])
#     msg.body = 'text body'#render_template(template + '.txt', **kwargs)
#     msg.html = '<b>HTML</b> body'#render_template(template + '.html', **kwargs)
#     mail.send(msg)

#define form class
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

#define model of role and user
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username

manager = Manager(app)
migrate = Migrate(app, db)

#add context for shell command
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command('shell', Shell(make_context=make_shell_context))

#add command for migrate
manager.add_command('db', MigrateCommand)
manager.run()


@app.route('/', methods=['GET','POST'])
def index():
    # msg = Message('subject', sender=os.environ.get('MAIL_USERNAME'), recipients=['401462312@qq.com'])
    # msg.body = 'text body'
    # msg.html = '<b>HTML</b> body'
    # mail.send(msg)
    return '<h1>ok!</h1>'
    # form = NameForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.name.data).first()
    #     if user is None:
    #         user = User(username=form.name.data)
    #         db.session.add(user)
    #         session['known'] = False
    #     else:
    #         session['known'] = True
    #     session['name'] = form.name.data
    #     form.name.data = ''
    #     return redirect(url_for('index'))
    # return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())
    # # # if form.validate_on_submit():
    #     old_name = session.get('name')
    #     if old_name is not None and old_name !=form.name.data:
    #         flash('Looks like you have changed your name!')
    #     session['name'] = form.name.data
    #     return redirect(url_for('index'))
    # return render_template('index.html', current_time=datetime.utcnow(), form = form, name = session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    #manager.run()
    app.run(debug=True)
