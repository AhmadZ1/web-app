from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

from config import app, db, users

login_BP = Blueprint("login_BP", __name__, static_folder="static", template_folder="templates")

@login_BP.route("/login", methods=["GET", "POST"])
def login():
  if "username" in session:
    flash("you are logged in!")
    return redirect(url_for("home"))
  if request.method == "POST":
    session.permanent = True
    username = request.form["username"]
    password = request.form["password"]
    #checks if the specified username is in the database
    found_user = users.query.filter_by(username=username).first()
    if found_user and password == found_user.password:
      session["username"] = username
      flash("login successfull!")
      return redirect(url_for("home"))
    else:
      return render_template("login.html", error="username or password are incorrect")
  return render_template("login.html")


