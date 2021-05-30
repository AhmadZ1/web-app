'''
file: helpers.py
description: contains some helper functions to be used in blueprints and main files
'''

from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

from config import app, db, users

def contains_digits(password):
  for i in password:
    if i.is_digit(): return True
  return False

'''helpers'''
def check_pass(password):
  '''cheks if the entered password is the same as the password for the account'''
  user = users.query.filter_by(username=session["username"]).first()
  return password == user.password

def get_credentials(username):
  '''gets the credentials of an account'''
  user = users.query.filter_by(username=username).first()
  return f"Username: {user.username}<br><br>Email: {user.email}<br><br>Password: {user.password}"

def pass_strength(password):
  '''checks if the password passes the minimum requirnments'''
  if len(password) < 8: return "Password length should be at least 8"
  if len(password.split()) > 1: return "Password can't contain spaces"
  if not contains_digits(password): return "Password should contains digits"
  return "good"

def get_user(username):
  '''gets the user object from the database'''
  return users.query.filter_by(username=username).first()