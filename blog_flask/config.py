import os
email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")
postgres_user = os.environ.get("POSTGRES_USER")
postgres_password = os.environ.get("POSTGRES_PASSWORD")

class Config:
    SECRET_KEY = '4caf8d2be717983770c235607a2fa9f7dab4b4b3fc13f7679c54e3d698ee5c45'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{postgres_user}:{postgres_password}@localhost/flask_blog"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG=True
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    MAIL_USERNAME=email
    MAIL_PASSWORD=password