from flask import Blueprint, render_template, redirect, url_for, flash
import flask_login as fl_log
from werkzeug.security import generate_password_hash
import crud
from forms import LoginForm, RegisterForm
from models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if fl_log.current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = form.user
        fl_log.login_user(user)
        return redirect(url_for('main.home'))
    return render_template('authentication/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if fl_log.current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        hashed_password = generate_password_hash(form.password.data)
        username = form.username.data
        user = User(email=email, password=hashed_password, username=username)
        crud.add_user(user)
        fl_log.login_user(user)
        return redirect(url_for('main.home'))
    return render_template('authentication/register.html', form=form)

@auth.route('/logout')
@fl_log.login_required
def logout():
    fl_log.logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))