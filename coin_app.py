from flask import Flask, render_template, url_for, flash, redirect
from forms import registration_form, login_form
from api_call import coin_json
app = Flask(__name__)

# Setting a secret key to guard our app against harm
app.config['SECRET_KEY'] = '78f5f532ab117b6910c29c480eb47b7b'

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

