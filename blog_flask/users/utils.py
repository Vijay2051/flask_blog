import os
import secrets

from flask import url_for
from flask_mail import Message
from PIL import Image

import blog_flask
from blog_flask import app, mail


# Method to save the incoming profile picture updated by the  user
def picture_save(picture):
    random_hex = secrets.token_hex(8)
    # this is an extension to split the incoming file into filename and extension
    _, f_ext = os.path.splitext(picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_filename)

    # Code to resize or scaledown the incoming  image to smaller sizes using pillow
    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename


def send_reset_password_token(user):
    token = user.get_reset_token()
    msg = Message("Password reset request",
                  sender=blog_flask.email, recipients=[user.email])
    print(user.email)
    msg.body = f"""
    To reset your password click this link: {url_for('users.reset_token', token=token, _external=True)}
    """
    mail.send(msg)
