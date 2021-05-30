from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

from config import app, db, users
from helpers import *

signup_BP = Blueprint("signup_BP", __name__, static_folder="static", template_folder="templates")

@signup_BP.route("/sign_up", methods=["GET", "POST"])
def signup():
  if "username" in session:
    flash("you are logged in!")
    return redirect(url_for("home"))
  if request.method == "POST":
    session.permanent = True
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    rpassword = request.form["password2"]
    username_exists = users.query.filter_by(username=username).first()
    email_exists = users.query.filter_by(email=email).first()
    if username_exists:
      return render_template("sign_up.html", error="username entered is not available")
    if email_exists:
      return render_template("sign_up.html", error="The email entered is associated with another account")
    if password != rpassword:
      return render_template("sign_up.html", error="Passwords don't match")
    if password == username or password == email:
      return render_template("sign_up.html", error="Password can't be same as username or email")
    result = pass_strength(password)
    if result != "good":
      return render_template("sign_up.html", error=result)
    session["username"] = username
    session["email"] = email
    usr = users(username, password, email)
    db.session.add(usr)
    db.session.commit()
    return redirect(url_for("home"))
  return render_template("sign_up.html")