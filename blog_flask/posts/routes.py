from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from wtforms.fields import Label

from blog_flask import db
from blog_flask.models import Post

from blog_flask.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        posts = Post(title=form.title.data,
                     content=form.content.data, author=current_user)
        db.session.add(posts)
        db.session.commit()
        flash("Your post is created!", "success")
        return redirect(url_for('main.home'))
    return render_template("create_post.html", title="New Post", legend='New Post', form=form)


@posts.route('/post/<int:post_id>')
def post(post_id):
    posts = Post.query.get_or_404(post_id)
    return render_template('post.html', title='Post', posts=posts)


@posts.route('/post/<int:post_id>/update', methods=["POST", "GET"])
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
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    # This is used to update the label in runtime
    form.submit.label = Label(field_id='submit', text="Update")
    return render_template('create_post.html', title='Update_Post', legend='Update Post', form=form)


@posts.route("/post/<int:post_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post is deleted successfully", "success")
    return redirect(url_for('main.home'))
