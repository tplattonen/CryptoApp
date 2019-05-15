from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# Setting a secret key to guard our app against harm
app.config['SECRET_KEY'] = '78f5f532ab117b6910c29c480eb47b7b'
# SQLite database to application, and a relative path for it
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///application.db'
db = SQLAlchemy(app)
# Bcrypt is used to hash applications passwords
bcrypt = Bcrypt(app)
# LoginManager is used handle user sessions
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# import routes after so we dont have circular import disaster
from cryptoapp import routes