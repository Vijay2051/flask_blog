import os
from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
# you could generate a secret key with secret.token_hex(some integer)
app.config['SECRET_KEY'] = '4caf8d2be717983770c235607a2fa9f7dab4b4b3fc13f7679c54e3d698ee5c45'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:suji2051@localhost/flask_blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# app.config['MAIL'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 
# app.config['MAIL_PASSWORD'] = 

email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = email,
    MAIL_PASSWORD = password
))

mail = Mail(app)


from blog_flask import routes