import os
import secrets

from flask import current_app
from flask import url_for
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from PIL import Image

from blog_flask import mail
from blog_flask.config import email


# Method to save the incoming profile picture updated by the  user
def picture_save(picture):
    random_hex = secrets.token_hex(8)
    # this is an extension to split the incoming file into filename and extension
    _, f_ext = os.path.splitext(picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_filename)

    # Code to resize or scaledown the incoming  image to smaller sizes using pillow
    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename


def send_reset_password_token(user):
    token = user.get_reset_token()
    msg = Message("Password reset request",
                  sender=email, recipients=[user.email])
    print(user.email)
    msg.body = f"""
    To reset your password click this link: {url_for('users.reset_token', token=token, _external=True)}
    """
    mail.send(msg)


def send_registration_token(email):
    s = Serializer(secret_key=current_app.config['SECRET_KEY'], expires_in=1800)
    token = s.dumps({"email": email}).decode("utf-8")
    msg = Message("Registration Request", sender=email, recipients=[email])
    msg.body = f"To confirm the registration process click the url gievn below: {url_for('users.register', token=token, _external=True)}"
    mail.send(msg)
