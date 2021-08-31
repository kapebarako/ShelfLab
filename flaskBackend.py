from flask import Flask, redirect, url_for, render_template, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy 
from datetime import  datetime
from enum import unique		#
import re			# regex
from string import printable #special char
import string

# Notes:
# Missing:		 Remember me (Login), Database
# env\Scripts\activate 
# python "test.py"   ---> debug on


# Create a Flask Instance
app = Flask(__name__, template_folder='template')
# Add database									username:passwrod@localhost/db name		
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost/users'
# Secret Key
app.config['SECRET_KEY'] = 'ilabshelflove'

# Initialize the Database
db = SQLAlchemy(app)

# # # Create Model for SQLA
# class Users(db.Model):                                            
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(100), nullable=False)
# 	email = db.Column(db.String(100), nullable=False, unique=True)
# 	date_added = db.Column(db.DateTime, default=datetime.utcnow)
	
# 	def __repr__(self):
# 		return '<Name %r>' % self.name

#  Signup Form Class   /userform tutorial
class SignupForm(FlaskForm):
	email = StringField("E-MAIL ADDRESS", validators=[DataRequired(), Length(min=2, max=20)])
	username = StringField("USERNAME", validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField('PASSWORD', validators=[DataRequired()])
	confirmpassword = PasswordField('CONFIRM PASSWORD', validators=[DataRequired()])
	submit = SubmitField("Sign Up")
	
#  Login Form Class
class LoginForm(FlaskForm):
	username = StringField("Username: ", validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField("Login")

#  Forgot Password Form Class
class forgotPassword(FlaskForm):
	email = StringField("E-MAIL ADDRESS", validators=[DataRequired(), Length(min=2, max=20)])
	submit = SubmitField("Continue")

#############

# Sign up Form
@app.route('/signup', methods=['GET','POST'])
def signup():
	account = None
	username = None		
	email = None
	password = None
	confirmpassword = None
	form = SignupForm()
	username = form.username.data
	email = form.email.data
	password = form.password.data
	confirmpassword = form.confirmpassword.data
	if form.validate_on_submit():
			# account = Users.query.filter_by(email=form.email.data).first()
			# account = Users(username = form.username.data, email = form.email.data, password = form.password.data)
			# db.session.add(account)
			# db.session.commit()
			form.email.data = ''			# clearing the form after submitting								
			form.username.data = ''															
			flash(f"Welcome to Shelflab, {username.capitalize()}. User added successfuly!")  # message that will flash
			# <a href="{{url_for('login')}}" class="alert-link">click to go back to the login page.</a>"
	return render_template("signup.html", form=form, account=account, username=username, password=password, confirmpassword=confirmpassword, email=email) #our_users=our_users

# Login Form
@app.route("/", methods=["POST", "GET"])
def login():
    return render_template('login.html')

# ForgotPassword Form
@app.route("/forgotpassword")
def forgotpassword():
    return render_template('forgotPassword.html')

# Homepage when login
@app.route("/<name>")
def user(name):
	return render_template("homePage.html", name=name)

# defaultTemplate
@app.route("/template")			
def template():
	return render_template("templatePage.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
	# db.create_all()
	app.run(debug=True, use_reloader=False)