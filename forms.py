# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('student', 'Student'), ('faculty', 'Faculty'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired(), Length(min=10, max=13)])
    publication_date = DateField('Publication Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Book')

class BorrowBookForm(FlaskForm):
    book_id = IntegerField('Book ID', validators=[DataRequired()])
    submit = SubmitField('Borrow Book')

class ReturnBookForm(FlaskForm):
    book_id = IntegerField('Book ID', validators=[DataRequired()])
    submit = SubmitField('Return Book')
