from flask import Blueprint, render_template, redirect, url_for, flash
from app import crud
from app.forms import PostForm
from app.models import BlogPost, db

main = Blueprint('main', __name__)

@main.route('/')
def home():
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
def make_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            author=form.author.data,
            img_url=form.img_url.data
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