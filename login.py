'''
file: login.py
type: blueprint
description: blueprint containing login function
'''

from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

from config import app, db, users

#creating blueprint
login_BP = Blueprint("login_BP", __name__, static_folder="static", template_folder="templates")

@login_BP.route("/login", methods=["GET", "POST"])
def login():
  '''allows user to login to his/her account'''
  #firsts checks if the user is already logged in
  if "username" in session:
    #flash() flashes a message to the page
    flash("you are logged in!")
    #redirect(url_for()) redirects to the specified function
    return redirect(url_for("home"))
  #checks if the page gives a post request
  if request.method == "POST":
    #gets the entered username and password from the form
    username = request.form["username"]
    password = request.form["password"]
    #checks if the specified username is in the database
    found_user = users.query.filter_by(username=username).first()
    #check if the user is found, and if the password entered matches the password of the account
    if found_user and password == found_user.password:
      #save the username to the session
      session["username"] = username
      #flash a message to let user know that he logged in successfully
      flash("login successfull!")
      #redirect user to home page
      return redirect(url_for("home"))
    else:
      #in case an error occured, show an error that username or password are incorrect
      return render_template("login.html", error="username or password are incorrect")
  #render the login.html template by default (in case no post requests)
  return render_template("login.html")


