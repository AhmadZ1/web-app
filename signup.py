'''
file: signup.py
type: blueprint
description: blueprint containing signup function
'''

from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

from config import app, db, users
from helpers import *

#creates blueprint
signup_BP = Blueprint("signup_BP", __name__, static_folder="static", template_folder="templates")

@signup_BP.route("/sign_up", methods=["GET", "POST"])
def signup():
  '''function to register new users'''
  #check if the user is logged in
  if "username" in session:
    #flashes a message to let user know they are logged in
    flash("you are logged in!")
    #redirects user to home page
    return redirect(url_for("home"))
  #checks if page gives post request
  if request.method == "POST":
    #makes session last longer, even if closed the browser 
    session.permanent = True
    #gets credentials from the form
    #username, email, password, and repeated password
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    rpassword = request.form["password2"]
    #check if username is already taken
    username_exists = users.query.filter_by(username=username).first()
    #check if email is already taken
    email_exists = users.query.filter_by(email=email).first()
    #if username already exists
    if username_exists:
      #give error that username is not available
      return render_template("sign_up.html", error="username entered is not available")
    #if email exists
    if email_exists:
      #give error that email is associated with another account
      return render_template("sign_up.html", error="The email entered is associated with another account")
    #check if password and repeated password are different
    if password != rpassword:
      #give error passwords don't match
      return render_template("sign_up.html", error="Passwords don't match")
    #check if password is same as username or email
    if password == username or password == email:
      #give error that password can't be same as username or email
      return render_template("sign_up.html", error="Password can't be same as username or email")
    #string holding the strength/error of the password
    #if the password is good it will be "good"
    #otherwise it will be the error that occured
    result = pass_strength(password)
    #if result is not "good"
    if result != "good":
      #give the specified error to the user
      return render_template("sign_up.html", error=result)
    #store username and email in the session
    session["username"] = username
    session["email"] = email
    #create user object with given username, email and password
    usr = users(username, password, email)
    #add user to the database
    db.session.add(usr)
    #commit changes to database
    db.session.commit()
    #flashes a message to let user know they signed up successfully
    flash("you have signed up successfully!")
    #redirect user to home page after successfully signing up
    return redirect(url_for("home"))
  #render the sign_up template in case no post request
  return render_template("sign_up.html")