from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required

from app import db
from app.forms.forms import LoginForm
from app.forms.forms import RegisterForm
from app.models.auth import User


@login_required
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


def register():
    form = RegisterForm()
    username = form.username.data
    password = form.password.data
    name = form.name.data
    email = form.email.data
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username, password, name, email)
            db.session.add(user)
            db.session.commit()

        return redirect(url_for('login'))

    else:
        return render_template('register.html', form=form)


def login():
    form = LoginForm()
    username = form.username.data
    password = form.password.data

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        
        if user and user.verify_password(password):
            login_user(user)
            flash("User logged-in!", 'info')
        else:
            flash("Username or password wrong!", 'warning')
    else:
        print(form.errors)

    return render_template('login.html', form=form)


def logout():
    logout_user()
    return redirect(url_for('login'))
