import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, abort, current_app
from flask_login import login_required
import flask_login as fl_log
from app import crud
from app.forms import PostForm
from app.models import BlogPost, db
from functools import wraps

main = Blueprint('main', __name__)

@main.route('/', defaults={'user_id': None})
@main.route('/user/<int:user_id>')
def home(user_id):
    if user_id:
        # Fetch posts by a specific user
        posts = crud.get_posts_by_user_id(user_id)
    else:
        # Fetch all posts
        posts = crud.get_all_posts()
    return render_template("index.html", all_posts=posts)

@main.route('/post/<int:post_id>')
def view_post(post_id):
    post = crud.get_post_by_id(post_id)
    return render_template("post.html", post=post)

@main.route('/about')
def about():
    return render_template("about.html")

@main.route('/contact')
def contact():
    return render_template("contact.html")

@main.route('/make-post', methods=["GET", "POST"])
@login_required
def make_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            author_id=fl_log.current_user.id,
            img_url=form.img_url.data,
            date=datetime.date.today()
        )
        db.session.add(new_post)
        db.session.commit()
        flash("New post created successfully!", "success")
        return redirect(url_for('main.view_post', post_id=new_post.id))
    return render_template(
        "post_form.html",
        form=form,
        heading="New Post",
        subheading="You're going to make a great blog post!",
        submit_text="Create Post",
        form_action=url_for('main.make_post')
    )

def owner_required(func):
    @wraps(func)
    def decorated_function(post_id, *args, **kwargs):
        # Ensure we're within an application context
        post = crud.get_post_by_id(post_id)  # Fetch post within the app context
        if post is None:
            abort(404)  # Handle case where post is not found
        if post.author_id != fl_log.current_user.id:
            abort(403)  # Forbidden access if the user is not the owner
        return func(post_id, *args, **kwargs)
    return decorated_function

@main.route('/edit-post/<int:post_id>', methods=["GET", "POST"])
@login_required
@owner_required
def edit_post(post_id):
    post = crud.get_post_by_id(post_id)

    form = PostForm(obj=post)  # Populate form with existing post data

    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.body = form.body.data
        post.author_id = fl_log.current_user.id
        post.img_url = form.img_url.data
        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for('main.view_post', post_id=post.id))

    return render_template(
        "post_form.html",
        form=form,
        heading="Edit Post",
        subheading="Update your blog post!",
        submit_text="Update Post",
        form_action=url_for('main.edit_post', post_id=post_id)
    )


@main.route('/delete-post/<int:post_id>')
@login_required
@owner_required
def delete_post(post_id):
    crud.delete_post(post_id)
    flash("Post deleted!", "success")
    return redirect(url_for('main.home'))