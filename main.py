'''
file: main.py
description: the main file that runs the app
'''

from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os

#import the app and database from config.py
from config import app, db, users

#importing and registering blueprints
from login import login_BP
from signup import signup_BP
from profile import profile_BP

app.register_blueprint(login_BP, url_prefix="")
app.register_blueprint(signup_BP, url_prefix="")
app.register_blueprint(profile_BP, url_prefix="")

app.permanent_session_lifetime = timedelta(days=5)



@app.route("/")
def home():
  '''Home page'''
  #checks if user is logged in
  if "username" in session:
    # renders home page
    return render_template("home.html")
  
  #redirect user to login page
  return redirect(url_for("login_BP.login"))


@app.route("/view")
def view():
  '''displays all the users, and their credentials, in the database'''
  return render_template("view.html", values=users.query.all())


@app.route("/logout")
def logout():
  '''logs out the user by removing his credentials from the session'''
  #checks if username is logged in
  if "username" in session:
    #remove the credentials from the session
    session.pop("username", None)
    session.pop("password", None)
    session.pop("email", None)
    #flash a message to let user know he/she have been logged out
    flash("You have been logged out!")
    #redirects user to login page
    return redirect(url_for("login_BP.login"))
  #if user isn't logged in flash a message to let user know he/she isn't logged in
  flash("You are not logged in!")
  #redirects user to login page
  return redirect(url_for("login_BP.login"))

#runs the app and creates the database
if __name__ == "__main__":
  db.create_all()
  port = int(os.environ.get("PORT", 5000))
  app.run(debug=True, host='0.0.0.0', port=port)