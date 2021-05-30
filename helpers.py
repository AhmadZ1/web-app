from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

from config import app, db, users

def check_pass(password):
  user = users.query.filter_by(username=session["username"]).first()
  return password == user.password

def change_password(new_pass):
  user = users.query.filter_by(username=session["username"]).first()
  user.password = new_pass
  db.session.commit()

def get_credentials(username):
  user = users.query.filter_by(username=username).first()
  return f"Username: {user.username}<br><br>Email: {user.email}<br><br>Password: {user.password}"

def pass_strength(password):
  if len(password) < 8: return "Password length should be at least 8"
  if len(password.split()) > 1: return "Password can't contain spaces"
  #add contain digits
  return "good"