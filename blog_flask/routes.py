import blog_flask
import os
import secrets
from PIL import Image

from flask import flash, redirect, render_template, request, url_for, abort
import flask
from flask_login import current_user, login_required, login_user, logout_user
from wtforms.fields import Label
from flask_mail import Message

from blog_flask import app, bcrypt, db, mail

from .forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm, ResetPasswordForm, RequestResetForm
from .models import Post, User


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get("page", default=1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Account is not valid, veliya poda ayogya rascal", "danger")
    return render_template('login.html', title='login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


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


@app.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        posts = Post(title=form.title.data,
                     content=form.content.data, author=current_user)
        db.session.add(posts)
        db.session.commit()
        flash("Your post is created!", "success")
        return redirect(url_for('home'))
    return render_template("create_post.html", title="New Post", legend='New Post', form=form)


@app.route('/post/<int:post_id>')
def post(post_id):
    posts = Post.query.get_or_404(post_id)
    return render_template('post.html', title='Post', posts=posts)


@app.route('/post/<int:post_id>/update', methods=["POST", "GET"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated", "success")
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    # This is used to update the label in runtime
    form.submit.label = Label(field_id='submit', text="Update")
    return render_template('create_post.html', title='Update_Post', legend='Update Post', form=form)


@app.route("/post/<int:post_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post is deleted successfully", "success")
    return redirect(url_for('home'))


@app.route("/user/<string:username>", methods=["GET", "POST"])
def author(username):
    page = request.args.get("page", default=1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('user_posts.html', posts=posts, user=user, user_det="____")



def send_reset_password_token(user):
    token = user.get_reset_token()
    msg = Message("Password reset request", sender = blog_flask.email, recipients=[user.email])
    print(user.email)
    msg.body=f"""
    To reset your password click this link: {url_for('reset_token', token=token, _external=True)}
    """
    mail.send(msg)


@app.route('/reset_password', methods=["GET", "POST"])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_password_token(user)
        flash("An email is sent to you with instructions to reset the password", "info")
        return redirect(url_for('login'))
    return render_template("reset_request.html", form=form, title='Reset Password')    


@app.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("This is an invalid or expired token", "warning")
        return redirect(url_for('reset_password'))
    form= ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Account password is changed for the user {user.username}!..You should login now!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)