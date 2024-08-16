from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from models import db, BlogPost
import crud
from forms import PostForm
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


if __name__ == "__main__":
    app.run(debug=True, port=5003)
