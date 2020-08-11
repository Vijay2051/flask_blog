from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from blog_flask import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expire_lim=1800):
        s = Serializer(
            secret_key=current_app.config['SECRET_KEY'], expires_in=expire_lim)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod  # this decorator tells python to dont expect self and to use without self arg
    def verify_reset_token(token):
        # refer the txt file for further clarification of how the data will be like and how to fetch the user_id from the token link
        s = Serializer(secret_key=current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception as e:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post ('{self.title}', '{self.date_posted}')"
