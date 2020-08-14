import os
email = "message.mail2051@gmail.com"
password = "suji2051"
postgres = os.environ.get['DATABASE_URL']

class Config:
    SECRET_KEY = '4caf8d2be717983770c235607a2fa9f7dab4b4b3fc13f7679c54e3d698ee5c45'
    SQLALCHEMY_DATABASE_URI = postgres
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG=True
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    MAIL_USERNAME=email
    MAIL_PASSWORD=password