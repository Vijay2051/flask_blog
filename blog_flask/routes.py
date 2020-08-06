from blog_flask import app
from .forms import RegistrationForm, LoginForm
from flask import render_template, url_for, redirect, flash
from .models import User, Post

posts = [
    {
        "title": "America got talent",
        "author": "Dave2D",
        "content": "Show that showcases all the talents in the World",
        "date_of_origin": "Oct_20_2016"
    },
    {
        "title": "Super singer",
        "author": "VijayTV",
        "content": "Show that showcases the music talents for TRP",
        "date_of_origin": "December_22_2008"
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "vijay@gmail.com" and form.password.data == "suji2051":
            flash("Account is Valid", "success")
            return redirect(url_for('home'))
        else:
            flash("Account is not valid, veliya poda ayogya rascal", "danger")
    return render_template('login.html', title='login', form=form)
