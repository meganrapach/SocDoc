from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    createAccount = SubmitField('Create Account')

class CreateAccountForm(FlaskForm):
    firstName = StringField('First Name', validators = [DataRequired()])
    lastName = StringField('Last Name', validators = [DataRequired()])
    zipCode = StringField('Zip', validators = [DataRequired()])
    email = StringField('Email Address', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Create Account')

class ContactUsForm(FlaskForm):
    name = StringField('Full Name', validators = [DataRequired()])
    email = StringField('Email Address', validators = [DataRequired()])
    message = TextAreaField('Message', validators = [DataRequired(), Length(min = 20, max=500)])
    submit = SubmitField('Send')
