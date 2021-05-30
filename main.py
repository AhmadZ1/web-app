from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

from config import app, db, users

from login import login_BP
from signup import signup_BP
from profile import profile_BP

app.register_blueprint(login_BP, url_prefix="")
app.register_blueprint(signup_BP, url_prefix="")
app.register_blueprint(profile_BP, url_prefix="")

app.permanent_session_lifetime = timedelta(days=5)


@app.route("/")
def home():
  return render_template("home.html")


@app.route("/view")
def view():
  return render_template("view.html", values=users.query.all())


@app.route("/logout")
def logout():
  if "username" in session:
    session.pop("username", None)
    session.pop("password", None)
    session.pop("email", None)
    flash("you have been logged out!")
    return redirect(url_for("login_BP.login"))
  flash("you are not logged in!")
  return redirect(url_for("login_BP.login"))


if __name__ == "__main__":
  db.create_all()
  app.run(debug=True)