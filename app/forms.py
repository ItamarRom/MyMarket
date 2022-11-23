# importing all the libraries we want to use for Form creation
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
import re

# This class is responsible for the construction of the Login Form
# Each variable is representing a field
# Each variable is an object of the imported fields at the top
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(),
    EqualTo('password')])
    submit = SubmitField('Register')

    #This function checks if the username submitted already exists
    def validate_username(self, username):
        # getting the user from DB using a query with the username as an argument
        # and checking if a user with the submitted username exists
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is already taken')
        if len(str(username.data)) < 4:
            raise ValidationError('Username must be at least 4 characters long')
        if not str(username.data).isalnum():
            raise ValidationError('Username may only contain letters and numbers')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user is not None:
            raise ValidationError('Email is already taken')


    def validate_password(self, password):
        """
        Verify the strength of 'password'
        Returns a dict indicating the wrong criteria
        A password is considered strong if:
            8 characters length or more
            1 digit or more
            1 symbol or more
            1 uppercase letter or more
            1 lowercase letter or more
        """
        # calculating the length
        length_error = len(str(password.data)) < 8

        # searching for digits
        digit_error = re.search(r"\d", str(password.data)) is None

        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", str(password.data)) is None

        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", str(password.data)) is None

        # searching for symbols
        symbol_error = re.search(r"\W", str(password.data)) is None

        # overall result
        password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

        if not password_ok:
            raise ValidationError('Password must contain at least 1 Upper and lower charecter , 1 special symbol and be at least 7 charecters long')






class ItemForm(FlaskForm):
    name = StringField('Item name', validators=[DataRequired(), Length(min=3)])
    price = IntegerField('price', validators=[DataRequired(message='Please enter a whole number.')])
    submit = SubmitField('Sell')


