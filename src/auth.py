from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from . import Usere
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    password = request.form.get("password")

    user = Usere.query.filter_by(email=email).first()

    if user:
        print("User already Exists")

    new_user = Usere(
        email=email, password=generate_password_hash(password, method="sha256")
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    user = Usere.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return redirect(url_for("auth.login"))

    login_user(user, remember=False)
    return redirect(url_for("main.profile"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
