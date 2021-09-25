from flask import render_template, redirect
from flask.helpers import flash, url_for
from app import app, bcrypt, db, login_manager
from app.models import User, Snippet
from app.forms import RegisterForm, LoginForm, SnippetForm
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)


@app.route("/")
def index():
    return render_template("home.html")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Ou, username or password not not seem to be correct")
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        db_user = User(username=form.username.data, password=hashed_password)
        print(db_user)
        db.session.add(db_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/paste-board")
@login_required
def paste_board():
    boards = Snippet.query.filter_by(user_id=current_user.id).order_by(Snippet.created_at.desc()).all()
    return render_template("paste_board.html", boards=boards)

@app.route("/paste", methods=["GET", "POST"])
@login_required
def create_snippet():
    form = SnippetForm()
    if form.validate_on_submit():
        snippet = Snippet(title=form.title.data, body=form.body.data, user_id=current_user.id)
        db.session.add(snippet)
        db.session.commit()
        return redirect(url_for("paste_board"))
    return render_template("paste.html", form=form)