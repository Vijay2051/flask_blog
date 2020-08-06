from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY']='4caf8d2be717983770c235607a2fa9f7dab4b4b3fc13f7679c54e3d698ee5c45'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from blog_flask import routes