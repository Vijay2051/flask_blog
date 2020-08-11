import os
from blog_flask.config import Config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# you could generate a secret key with secret.token_hex(some integer)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail(app)

from blog_flask.users.routes import users
from blog_flask.posts.routes import posts
from blog_flask.main.routes import main
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
