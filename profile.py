from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

from config import app, db, users
from helpers import *

profile_BP = Blueprint("profile_BP", __name__, static_folder="static", template_folder="templates/profile")

@profile_BP.route("/Profile")
def profile():
  if "username" in session:
    return render_template("profile.html", username=session["username"])
  flash("You are not logged in")
  return redirect(url_for("home"))

@profile_BP.route("/change_password", methods=["GET", "POST"])
def change_pass():
  if request.method == "POST":
    password = request.form["old_password"]
    username = session["username"]
    if check_pass(password):
      return redirect(url_for("profile_BP.new_pass"))
    else: return render_template("change_pass.html", error="Incorrect password")
  return render_template("change_pass.html")

@profile_BP.route("/new_pass", methods=["GET", "POST"])
def new_pass():
  if request.method == "POST":
    new_password = request.form["new_pass"]
    rnew_password = request.form["new_pass2"]
    if new_password != rnew_password:
      return render_template("new_pass.html", error="passwords don't match")
    user = users.query.filter_by(username=session["username"]).first()
    if user.username == new_password or user.email == new_password:
      return render_template("new_pass.html", error="password can't be same as username or email")
    user.password = new_password
    db.session.commit()
    flash("Password changed successfully!")
    return redirect(url_for("profile_BP.profile"))
  return render_template("new_pass.html")

@profile_BP.route("/credentials", methods=["GET", "POST"])
def credentials():
  if request.method == "POST":
    password = request.form["password"]
    if check_pass(password):
      return get_credentials(session["username"])
    else: return render_template("get_pass.html", error="Incorrect password")
  return render_template("get_pass.html")