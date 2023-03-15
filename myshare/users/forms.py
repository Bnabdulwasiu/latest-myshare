from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password:",
                                    validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign up")
    
class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired()])
    remember = BooleanField("Remember Me:")
    submit = SubmitField("Login")

class UpdateUserAccount(FlaskForm):
    username = StringField("Username:", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")
    
class RequestResetForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")
    

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password:", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password:",
                                    validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")