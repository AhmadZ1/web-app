'''
file: profile.py
description: contains functions to do actions related to the profile (change password, change email, change username, ...etc)
'''

from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

from config import app, db, users
from helpers import *

#create blueprint
profile_BP = Blueprint("profile_BP", __name__, static_folder="static", template_folder="templates/profile")

@profile_BP.route("/Profile")
def profile():
  '''renders profile page'''
  #check if user is logged in
  if "username" in session:
    #render profile page for the user
    return render_template("profile.html", username=session["username"])
  #otherwise user is not logged in
  #redirects user to home page
  return redirect(url_for("home"))

@profile_BP.route("/get_password/<reason>", methods=["GET", "POST"])
def get_pass(reason):
  print(reason)
  '''requests the old password from user to check if they can change the password or not'''
  #if page gives post request
  if request.method == "POST":
    #gets password from the form
    password = request.form["password"]
    # checks if admin is logging in to view accounts' credentials
    if reason == "is_admin":
      admin = get_user("admin")
      if password == admin.password:
        return render_template("view.html", values=users.query.all())
      flash("You are not admin")
      return redirect(url_for("view"))
    # checks if password entered is same as password of user's account (helper function)
    if check_pass(password):
      #if the reason was to change the password
      if reason == "new_pass":
        #redirect user to page to choose new password
        return redirect(url_for("profile_BP.new_pass"))
      elif reason == "del_acc":
        session["delete_account_key"] = "ad64fa64dsasf4da64"
        #redirect user to delete account
        return redirect(url_for("profile_BP.are_you_sure"))
    #otherwise if password doesn't match user's password, give Incorrect password error
    return render_template("change_pass.html", error="Incorrect password")
  #render change_pass template by default (when no post request)
  return render_template("get_pass.html")

@profile_BP.route("/new_pass", methods=["GET", "POST"])
def new_pass():
  '''changes user's password (called from change_pass() only)'''
  #if page gives post request
  if request.method == "POST":
    #get new password and repeated new password from the form
    new_password = request.form["new_pass"]
    rnew_password = request.form["new_pass2"]
    #if passwords don't match
    if new_password != rnew_password:
      #give error that passwords don't match
      return render_template("new_pass.html", error="passwords don't match")
    #check if the password is good
    result = pass_strength(new_password)
    if result != "good":
      #if not good give the specified error to the user
      return render_template("new_pass.html", error=result)
    #get the user from the database
    user = get_user(session["username"])
    #check if the user's username or email is same as chosen new password
    if user.username == new_password or user.email == new_password:
      #give error that password can't be same as username or email
      return render_template("new_pass.html", error="password can't be same as username or email")
    #change user's password
    user.password = new_password
    #commit changes to database
    db.session.commit()
    #give message that password was changed successfully
    flash("Password changed successfully!")
    #redirect user to profile page
    return redirect(url_for("profile_BP.profile"))
  #by default render the new_pass template
  return render_template("new_pass.html")

@profile_BP.route("/credentials", methods=["GET", "POST"])
def credentials():
  '''displays user's username, email, and password'''
  #if page gives post request
  if request.method == "POST":
    #ask user for password
    #gets password from the form
    password = request.form["password"]
    #check if passwords match
    if check_pass(password):
      #redirects user to page containing their credentials
      return get_credentials(session["username"])
    #otherwise give error Incorrect password
    return render_template("get_pass.html", error="Incorrect password")
  #by default render the get_pass template
  return render_template("get_pass.html")


@profile_BP.route("/are_you_sure", methods=["GET", "POST"])
def are_you_sure():
  '''ask user to confirm their account deletion'''
  if request.method == "POST":
    if "delete_account_key" in session:
      return redirect(url_for("profile_BP.del_acc"))
  return render_template("confirm.html")

@profile_BP.route("/delete_account")
def del_acc():
  '''deletes user's account'''
  if "delete_account_key" in session:
    user = get_user(session["username"])
    session.pop("delete_account_key", None)
    session.pop("username", None)
    session.pop("password", None)
    session.pop("email", None)
    db.session.delete(user)
    db.session.commit()
    flash("account deleted")
    return redirect(url_for("login_BP.login"))
  flash("Please confirm your Password first")
  return redirect(url_for("profile_BP.get_pass", reason="del_acc"))