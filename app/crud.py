from .models import db, BlogPost, User
from datetime import date

# Function to get all blog posts
def get_all_posts():
    return BlogPost.query.all()

# Function to get a single post by ID
def get_post_by_id(post_id):
    return BlogPost.query.get_or_404(post_id)

def get_posts_by_user_id(user_id):
    return BlogPost.query.filter_by(author_id=user_id).all()


# Function to create a new post
def add_new_post(title, subtitle, body, author, img_url):
    new_post = BlogPost(
        title=title,
        subtitle=subtitle,
        date=date.today().strftime("%B %d, %Y"),
        body=body,
        author=author,
        img_url=img_url
    )
    db.session.add(new_post)
    db.session.commit()

# Function to edit a post
def edit_post(post_id, title, subtitle, body, author, img_url):
    post = BlogPost.query.get(post_id)
    post.title = title
    post.subtitle = subtitle
    post.body = body
    post.author = author
    post.img_url = img_url
    db.session.commit()

# Function to delete a post
def delete_post(post_id):
    post = BlogPost.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

# Users ---------------------------------------------------------------------------


def add_user(user):
    # Assuming `user` is an instance of the User model
    db.session.add(user)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def email_exists(email):
    return User.query.filter_by(email=email).first() is not None
