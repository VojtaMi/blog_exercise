from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from .models import db
from .routes import init_routes

load_dotenv()

bootstrap = Bootstrap5()
login_manager = LoginManager()
ckeditor = CKEditor()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Set Flask configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Initialize extensions
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    init_routes(app)

    # Create database tables (optional)
    with app.app_context():
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    return crud.get_user_by_id(user_id)