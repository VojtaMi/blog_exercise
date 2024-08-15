from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from models import db
import crud
from forms import CreatePostForm
from flask_ckeditor import CKEditor


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

# Initialize extensions
db.init_app(app)
Bootstrap5(app)

# Initialize CKEditor
ckeditor = CKEditor(app)

# Make sure the database is created before the first request
with app.app_context():
    db.create_all()


# ROUTES
@app.route('/')
def home():
    posts = crud.get_all_posts()
    return render_template("index.html", all_posts=posts)


@app.route('/post/<int:post_id>')
def show_post(post_id):
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
    form = CreatePostForm()
    if form.validate_on_submit():
        # Add the post to the database
        crud.add_new_post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            author=form.author.data,
            img_url=form.img_url.data
        )
        flash("Your post has been successfully created!", "success")
        return redirect(url_for('home'))

    return render_template("make-post.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
