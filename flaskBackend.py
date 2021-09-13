from flask import Flask, redirect, url_for, render_template, request, flash, session
from datetime import timedelta
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from enum import unique		#
import re			# regex
from string import printable #special char
import string
import csv
import sqlite3
import os
import smtplib
import sqlalchemy as db

# Notes:
# env\Scripts\activate 
# python flaskBackend.py   ---> debug on
# pop up t&c pp



# Create a Flask Instance
app = Flask(__name__, template_folder='template')
# Secret Key
app.secret_key = "ilabshelflove"
# Add database								     username:password@localhost/db name		
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Gonzales2001@localhost/shelflab'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Sessions timer
app.permanent_session_lifetime = timedelta(minutes=5)
# Initialize the Database
db = SQLAlchemy(app)

# python -i     	# for winpty python

# Create Model for SQLA
class users(db.Model):                                            
	uid = db.Column(db.Integer, primary_key=True) 					# must be autoincrement
	email = db.Column(db.String(100), nullable=False, unique=True)
	username = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String(100), nullable=False)
	date_added = db.Column(db.DateTime, default=datetime.utcnow) 	# added


	def __repr__(self):
		return '<Name %r>' % self.username


#  Signup Form Class   /userform tutorial
class SignupForm(FlaskForm):
	email = StringField("E-MAIL ADDRESS")
	username = StringField("USERNAME")
	password = PasswordField('PASSWORD')
	submit = SubmitField("Sign Up")
	
#  Login Form Class
class LoginForm(FlaskForm):
	username = StringField("Username: ")
	password = PasswordField("Password")
	remember = BooleanField('Remember Me')
	submit = SubmitField("Login")

#  Forgot Password Form Class
class forgotPassword(FlaskForm):
	email = StringField("E-MAIL ADDRESS", validators=[DataRequired(), Length(min=2, max=20)])
	submit = SubmitField("Continue")

#############

# @app.route("/accounts",	methods=["POST","GET"])
# def accounts():
#     return render_template("accounts.html", accounts=accounts)

# Sign up Form
@app.route("/signup", methods=["GET","POST"]) # get post?
def signup():
	form = SignupForm()
	username = form.username.data
	email = request.form.get("email")
	username = request.form.get("username")
	password = request.form.get("password")
	if form.validate_on_submit():
		# user = users.query.filter_by(email=form.email.data).first()
		# if user is None:
			# accounts.append(username)
			user = users(email=form.email.data, username=form.username.data, password=form.password.data)
			db.session.add(user)
			db.session.commit()
			server= smtplib.SMTP("smtp.gmail.com", 587)
			server.starttls()
			server.login("shelflab.ue@gmail.com","IlabShelflove") 	# for logging account  (username,pw)
			server.sendmail("shelflab.ue@gmail.com", email, "Your account is successfully created!")
			flash(f"Welcome to Shelflab, {username.capitalize()}. User added successfuly!")
	our_users = users.query.order_by(users.date_added)
	return render_template("signup.html", form=form, username=username, password=password, email=email, our_users=our_users)

# Login Form
@app.route("/", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session.permanent = True
		user = request.form['username']
		session['user'] = user
		return redirect(url_for('user'))
	else:
		if "user" in session:
			return redirect(url_for('user'))
		return render_template('login.html')

# Homepage when login
@app.route("/homepage")
def user():
	if 'user' in session:
		user = session['user']
		return render_template("overview.html", name=user)
	else:								# login again
		return redirect(url_for('login'))

@app.route("/logout")
def logout():
	session.pop('user', None)
	return redirect(url_for("login"))


# ForgotPassword Form
@app.route("/forgotpassword")
def forgotpassword():
    return render_template('forgotPassword.html')

# defaultTemplate
@app.route("/template")			
def template():
	return render_template("templatePage.html")

@app.route("/termsnconditions")			
def termsncondition():
	return render_template("termsnconditions.html")

@app.errorhandler(404)
def page_not_found(e):
    # return render_template(""), 404
	return "Error 404, Not Found"

@app.errorhandler(500)
def page_not_found(e):
    # return render_template("500.html"), 500
	return "Error 500, Internal Server Error"

if __name__ == "__main__":
	# db.create_all()
	app.run(debug=True, use_reloader=False)	