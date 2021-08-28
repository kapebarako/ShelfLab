from flask import Flask, redirect, url_for, render_template, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from forms import RegistrationForm, LoginForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy 
from datetime import  datetime

# Create a Flask Instance
app = Flask(__name__, template_folder='template')
# Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Secret Key
app.config['SECRET_KEY'] = 'ilabshelflove'


# SQLALCHEMY_TRACK_MODIFICATIONS = False
# bootstrap = Bootstrap(app)

# Initialize the Database
db = SQLAlchemy(app)


# Create Model for SQLA
class Users(db.Model):                                            
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), nullable=False, unique=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)
	
	def __repr__(self):
		return '<Name %r>' % self.name



#  Signup Form Class   /userform tutoiral
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



#############


# Sign up Form      /add
@app.route('/signup', methods=['GET','POST'])
def signup():
	name = None
	form = SignupForm()
	if form.validate_on_submit():   
		user = Users.query.filter_by(email=form.username.data).first()
		if user is None:																# username not exist
			user = Users(email=form.email.data, username=form.username.data, password=form.password.data, confirmpassword=form.confirmpassword.data) #inputs from signup.html
			db.session.add(user)
			db.session.commit()
		name = form.name.data 				#successfully added then will clear the form
		form.email.data = ''															
		form.username.data = ''															
		form.password.data = ''
		form.confrimpassword.data = ''
		flash("User added successfully!") 
	our_users = Users.query.order_by(Users.date_added)
	return render_template("signup.html",form=form, name=name, our_users=our_users)



# Login form
@app.route("/", methods=["POST", "GET"])
def login():
    return render_template('login.html')
    # return redirect(url_for('user'))


# defaultTemplate
@app.route("/template")			
def template():
	return render_template("templatePage.html")


# homepage when login
@app.route("/<name>")	#, methods=['GET', 'POST']		
def user(name):
	return render_template("homePagee.html", name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
	# db.create_all()
	app.run(debug=True, use_reloader=False)