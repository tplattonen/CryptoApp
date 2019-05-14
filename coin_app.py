from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import registration_form, login_form
from api_call import coin_json

app = Flask(__name__)
# Setting a secret key to guard our app against harm
app.config['SECRET_KEY'] = '78f5f532ab117b6910c29c480eb47b7b'
# SQLite database to application, and a relative path for it
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///application.db'
db = SQLAlchemy(app)

# Database structure
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # Relation ship to Post model
    posts = db.relationship('Post', backref='author', lazy=True)

def __repr__(self):
    return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def __repr__(self):
    return f"Post('{self.title}', '{self.date_posted}', '{self.content}')"

# Coinmarketcap json
coins = coin_json

#Route for home page
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", coins=coin_json)

#Route for about page
@app.route("/about")
def about():
    return render_template("about.html", title='About')

#Route for register page
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = registration_form()
    if form.validate_on_submit():
        flash(f'Account greated successfully for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

#Route for login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = login_form()
    if form.validate_on_submit():
        if form.email.data == 'admin@coin.com' and form.password.data == 'password':
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

# Makes application run straight through python
if __name__ == "__main__":
    # Uses debug mode so its not necessary restart app everytime we make changes to be able to see them
    app.run(debug=True)

