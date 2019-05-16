import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from cryptoapp.forms import registration_form, login_form, update_account_form
from cryptoapp import app, db, bcrypt
from cryptoapp.models import User, Post
from cryptoapp.api_call import coin_json
from flask_login import login_user, current_user, logout_user, login_required

# Coinmarketcap json
coins = coin_json



#Route for home page
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", coins=coin_json)

# Route for about page
@app.route("/about")
def about():
    return render_template("about.html", title='About')

# Route for register page
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = registration_form()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created successfully! You may enter!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# Route for login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page =  request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


# Route for logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# Function to save uploaded profile picture to file system
def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # To make sure that picture file is saved with same extension as it was uploaded (i.e gif, png).
    # form_picture is data from the submitted field
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', 'profile_images', picture_filename)

    # Resize large images if its not .gif file since it will be broken.
    if f_ext == '.gif':
        form_picture.save(picture_path)
    else:
        output_size = (125, 125)
        rimage = Image.open(form_picture)
        rimage.thumbnail(output_size)

        rimage.save(picture_path)
    return picture_filename


# Route for account page
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = update_account_form()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Great! Account updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_images/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)