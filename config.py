'''
file: config.py
description: initialises the app and database to be imported fro mother files
(the main goal is to avoid circular imports between main.py and blueprints files)
'''

from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

#creating flask app and setting a secret key
app = Flask(__name__)
app.secret_key = "dflja5a54asfa13df645d"
#choose the name of the database and connecting it to the app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#database object
class users(db.Model):
  #specifies database columns
  _id = db.Column("id", db.Integer, primary_key=True) 
  username = db.Column("username", db.String(100))
  password = db.Column("password", db.String(100))
  email = db.Column("email", db.String(200))
  
  def __init__(self, username, password, email):
    self.username = username
    self.password = password
    self.email = email
