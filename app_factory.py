from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from models import db
import crud

load_dotenv()

# Initialize extensions but do not bind them to the app yet
bootstrap = Bootstrap5()
login_manager = LoginManager()
ckeditor = CKEditor()
migrate = Migrate()

def create_app():
    # Create the Flask app instance
    app = Flask(__name__)

    # Set Flask configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Initialize extensions with the app instance
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Load the blueprints (if you are using them)
    # from your_project.auth import auth_bp
    # app.register_blueprint(auth_bp)

    # Load the routes
    from . import routes
    routes.init_app(app)

    # Create database tables (optional, can be moved elsewhere)
    with app.app_context():
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    return crud.get_user_by_id(user_id)

