from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import current_app
from blog_flask import bcrypt, db
from blog_flask.models import Post, User
from blog_flask.users.forms import (ConfirmRegisterForm, LoginForm,
                                    RegistrationForm, RequestResetForm,
                                    ResetPasswordForm, UpdateAccountForm)
from blog_flask.users.utils import (picture_save, send_registration_token,
                                    send_reset_password_token)

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def confirm_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ConfirmRegisterForm()
    if form.validate_on_submit():
        send_registration_token(form.email.data)
        flash("An email for the registration link is sent to you, Check your email and click the Link to proceed the registration", "info")
        return redirect(url_for('users.confirm_register'))
    return render_template("register_confirm.html", form=form)


@users.route("/register/<token>", methods=['POST', 'GET'])
def register(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    s = Serializer(secret_key=current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token)['email']
    except Exception as e:
        flash("This is an invalid or expired token..if you opt for registration submit your mail, get the link and fill the credentials within 30 mins", "danger")
        return redirect(url_for('users.confirm_register'))
    print(email)
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Account is not valid, veliya poda ayogya rascal", "danger")
    return render_template('login.html', title='login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = picture_save(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account is successfully updated", "success")
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@users.route("/user/<string:username>", methods=["GET", "POST"])
def author(username):
    page = request.args.get("page", default=1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('user_posts.html', posts=posts, user=user, user_det="____")


@users.route('/reset_password', methods=["GET", "POST"])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_password_token(user)
        flash("An email is sent to you with instructions to reset the password", "info")
        return redirect(url_for('users.login'))
    return render_template("reset_request.html", form=form, title='Reset Password')


@users.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("This is an invalid or expired token", "warning")
        return redirect(url_for('users.reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(
            f'Account password is changed for the user {user.username}!..You should login now!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
