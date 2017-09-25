from flask import Flask
from flask_mail import Mail, Message
import os


app = Flask(__name__)

#下面是SMTP服务器配置
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.126.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER = 'Admin<pythonflasktest@126.com>'
))
mail = Mail(app)

@app.route('/')
def index():
    msg = Message('Subject', recipients=['401462312@qq.com'])
    msg.body = 'text body'
    try:
        mail.send(msg)
        return '<h1>sent</h1>'
    except ValueError:
        print('sorry')



if __name__ == '__main__':
    app.run()
