from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from models import db, BlogPost, User
import crud
from forms import PostForm, LoginForm
from flask_ckeditor import CKEditor
import os
from dotenv import load_dotenv
import flask_login as fl_log
from flask_migrate import Migrate

# Load environment variables from the .env file
load_dotenv()

# Access the variables
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

app = Flask(__name__)

migrate = Migrate(app, db)

# Set Flask configuration
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# Initialize extensions
Bootstrap5(app)
db.init_app(app)  # This should come after setting the config
ckeditor = CKEditor(app)

# Make sure the database is created before the first request
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@app.context_processor
def inject_user():
    return {'current_user': fl_log.current_user}


@login_manager.user_loader
def load_user(user_id):
    return crud.get_user_by_id(user_id)


# ROUTES
@app.route('/')
def home():
    posts = crud.get_all_posts()
    return render_template("index.html", all_posts=posts)


@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = crud.get_post_by_id(post_id)
    return render_template("post.html", post=post)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/make-post', methods=["GET", "POST"])
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
        return redirect(url_for('view_post', post_id=new_post.id))

    return render_template(
        "post_form.html",
        form=form,
        heading="New Post",
        subheading="You're going to make a great blog post!",
        submit_text="Create Post",
        form_action=url_for('make_post')
    )


@app.route('/edit-post/<int:post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    post = crud.get_post_by_id(post_id)

    form = PostForm(obj=post)  # Populate form with existing post data

    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.body = form.body.data
        post.author = form.author.data
        post.img_url = form.img_url.data
        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for('view_post', post_id=post.id))

    return render_template(
        "post_form.html",
        form=form,
        heading="Edit Post",
        subheading="Update your blog post!",
        submit_text="Update Post",
        form_action=url_for('edit_post', post_id=post_id)
    )


@app.route('/delete-post/<int:post_id>')
def delete_post(post_id):
    crud.delete_post(post_id)
    flash("Post deleted!", "success")
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect already logged-in users
    if fl_log.current_user.is_authenticated:
        return redirect(url_for('home'))  # Redirect to a protected page or dashboard

    form = LoginForm()  # Create an instance of the LoginForm

    if form.validate_on_submit():  # This triggers validation, including custom validators
        user = form.user  # Access the user object from custom validation

        # Log in the user
        fl_log.login_user(user)

        return redirect(url_for('home'))  # Redirect to a protected page or dashboard

    return render_template('authentication/login.html', form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
