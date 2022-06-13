from email.policy import default
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerRangeField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class AddNewBeerForm(FlaskForm):
    beer_name = StringField(label = "Beer Name", validators=[DataRequired()])
    brewery_name = StringField(label = "Brewery Name", validators=[DataRequired()])
    beer_style = StringField(label = "Beer Style", validators=[DataRequired()])
    beer_comment = TextAreaField(label = "Comment", validators=[DataRequired(), Length(min=15, max=200, message="Your comment should have min. 15 and max. 200 chars!")])
    beer_rate = IntegerRangeField(label = "Beer Rate", default = 5)
    submit = SubmitField("Submit")

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
